from django.shortcuts import redirect, render,get_object_or_404
from .models import BookingSlotTable as BookingSlot
from .models import UserBookingTable as userBooking
from turfowner.models import turf_table



# def bookslots(request, id):
#     # Get the turf instance
#     turf = get_object_or_404(turf_table, id=id)

#     if request.method == "POST":
#         # Get the selected slot IDs from the form (list of selected slot start times)
#         selected_slots = request.POST.getlist("slot_ids[]")
#         print("Selected slots:", selected_slots)
#         booking_slot_table = BookingSlot.objects.filter(turf=turf, expired=False).first()

       
#         if booking_slot_table:
#             updated_slots = []  # This will store the updated slot data
#             booked_slots = []  # This will store the booked slot details

#             for slot in booking_slot_table.slots:

#                 # Check if the slot is selected and available
#                 if slot['start_time'] in selected_slots and slot['status'] == "available":
                    

#                     slot['status'] = "booked"
#                     slot['user']=request.user.username

#                     # Create a dictionary for booked slots to be stored in userBooking
#                     userslot_dict = {
#                         'start_time': slot['start_time'],
#                         'end_time': slot['end_time'],
#                         'user':request.user.username,
#                         'expired': False
#                     }
#                     booked_slots.append(userslot_dict)  # Add to booked slots

#                 updated_slots.append(slot)  # Add slot to updated list (whether booked or not)
           
#             # Calculate the total amount based on the number of booked slots
#             amount = len(booked_slots) * int(turf.rent)

#             # Create a user booking record
#             bid=userBooking.objects.create(
#                 turfname=turf,
#                 customer=request.user,
#                 slots=booked_slots,
#                 amount=amount  # Adjust the amount if needed
#             )

#             # Save the updated slots back to the BookingSlotTable instance
#             booking_slot_table.slots = updated_slots
#             booking_slot_table.save()

#             context = {
#                 'amount': amount,
#                 'bid':bid.id
#             }

#             # Return a success response
#             return render(request, 'bookingsuccess.html', context)
        
# def payment_success(request):
#     payment_id = request.GET.get('payment_id')
#     bid = request.GET.get('bid')

#     # Retrieve the booking by bid
#     booking = userBooking.objects.get(id=bid)

#     # You can update the payment status or mark the booking as paid
#     booking.payment_status = "Paid"  # Update booking payment status (you need to have this field)
#     booking.payment_id = payment_id  # Store the Razorpay payment ID
#     booking.save()

#     return render(request, 'payment_success.html', {'payment_id': payment_id, 'bid': bid})
import razorpay
from django.shortcuts import render, get_object_or_404

RAZORPAY_KEY_ID = 'rzp_test_X5OfG2jiWrAzSj'
RAZORPAY_KEY_SECRET = 'SsCovWWZSwB1TGd1rSoIiwF3'

def bookslots(request, id):
    # Get the turf instance
    turf = get_object_or_404(turf_table, id=id)

    if request.method == "POST":
        # Get the selected slot IDs from the form (list of selected slot start times)
        selected_slots = request.POST.getlist("slot_ids[]")
        print("Selected slots:", selected_slots)
        booking_slot_table = BookingSlot.objects.filter(turf=turf, expired=False).first()

        if booking_slot_table:
            updated_slots = []  # This will store the updated slot data
            booked_slots = []  # This will store the booked slot details

            for slot in booking_slot_table.slots:
                # Check if the slot is selected and available
                if slot['start_time'] in selected_slots and slot['status'] == "available":
                    slot['status'] = "booked"
                    slot['user'] = request.user.username

                    # Create a dictionary for booked slots to be stored in userBooking
                    userslot_dict = {
                        'start_time': slot['start_time'],
                        'end_time': slot['end_time'],
                        'user': request.user.username,
                        'expired': False
                    }
                    booked_slots.append(userslot_dict)  # Add to booked slots

                updated_slots.append(slot)  # Add slot to updated list (whether booked or not)

            # Calculate the total amount based on the number of booked slots
            amount = len(booked_slots) * int(turf.rent)

            # Initialize Razorpay client with your Razorpay Key ID and Secret
            razorpay_client = razorpay.Client(auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET))

            # Create an order on Razorpay
            order = razorpay_client.order.create({
                'amount': amount * 100,  # Amount in paise
                'currency': 'INR',
                'payment_capture': '1'  # Automatic payment capture
            })

            razorpay_order_id = order['id']  # Order ID from Razorpay

            # Create a user booking record (but mark it as 'pending' for now)
            bid = userBooking.objects.create(
                turfname=turf,
                customer=request.user,
                slots=booked_slots,
                amount=amount,
                payment_id=razorpay_order_id,  # Store Razorpay order ID
            )

            # Save the updated slots back to the BookingSlotTable instance
            booking_slot_table.slots = updated_slots
            booking_slot_table.save()

            context = {
                'amount_display': amount,        # e.g., 120
                'amount': amount * 100,  # Pass the amount in paise (already calculated)
                'bid': bid.id,
                'razorpay_order_id': razorpay_order_id,
                'razorpay_key': RAZORPAY_KEY_ID,
            }
            return render(request, 'bookingsuccess.html', context)


        else:
            # Handle the case when booking slots are unavailable
            return render(request, 'booking_error.html', {'error': 'No available slots for your selection.'})

def payment_success(request):
    payment_id = request.GET.get('payment_id')
    bid = request.GET.get('bid')

    # Retrieve the booking by bid (it should be in "pending" state)
    booking = userBooking.objects.get(id=bid)

    # Check if the payment was successful (optional step: verify payment status with Razorpay API)
    razorpay_client = razorpay.Client(auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET))
    payment = razorpay_client.payment.fetch(payment_id)

    if payment['status'] == 'captured':
        # If payment is captured, update the booking to 'paid'
        booking.status = 'paid'  # Change the booking status to 'paid'
        booking.payment_id = payment_id  # Store the Razorpay payment ID
        booking.save()

        # Here, you can also send a confirmation email to the user, or do any other actions
        return redirect('userbookings')

    else:
        # If payment failed, show failure message
        booking.status = 'failed'  # Update status to 'failed'
        booking.save()
        return render(request, 'payment_failure.html', {'payment_id': payment_id, 'bid': bid})


def userbookings(request):
    bookings=userBooking.objects.filter(customer=request.user).all()

    return render(request,'mybooking.html',{'bookings':bookings})


def addname(request,bid):
    bookings=userBooking.objects.get(id=bid)

    if request.method=='POST':
        name=request.POST['name']

        bookings.name=name
        bookings.save()

        
        booking=userBooking.objects.filter(customer=request.user).all()
  
        return render(request,'mybooking.html',{'bookings':booking}) 


def cancelbooking(request, tid, bid):

    turf = get_object_or_404(turf_table, id=tid)
    booking_slot = get_object_or_404(BookingSlot, turf=turf, expired=False)
    userbook=userBooking.objects.get(id=bid)
    for i in userbook.slots:
        print(i['start_time'])

        for slots in booking_slot.slots:
             if slots['start_time']==i['start_time']:
                 slots['status']='available'
                 slots['user']=None
    turf.slots=True
    turf.save()             

    booking_slot.save()         
    userbook.delete()

    bookings=userBooking.objects.filter(customer=request.user).all()
  
    return render(request,'mybooking.html',{'bookings':bookings})
   
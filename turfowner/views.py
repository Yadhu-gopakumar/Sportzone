from django.shortcuts import render,redirect,get_object_or_404

from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.utils.dateformat import format
from .form import turfForm
from .models import turf_table,reviewtable
from booking.models import BookingSlotTable as BookingSlot,UserBookingTable
from datetime import datetime, timedelta

# Create your views here.


@login_required(login_url='ownerlogin')
def ownerhome(request):
    return render(request,'turfowner.html')

@login_required(login_url='ownerlogin')
def ownersearchturf(request):
    userturf=turf_table.objects.filter(ownername=request.user).all()
    context={'turfs':userturf}
    if 'query' in request.GET:
        q=request.GET['query']
   
        res=turf_table.objects.filter(name__icontains=q) | turf_table.objects.filter(location__icontains=q) and turf_table.objects.filter(ownername=request.user) 
   
        if res is not None:
            context={
                'turfs':res,
                    }
        else:
            context={
            'turfs':res,
                }  
            
        return render(request,'ownerturflist.html',context)
    return render(request,'ownerturflist.html',context)

def addturf(request):
    if request.method=='POST':
        turf_name=request.POST['turf_name']
        game_type=request.POST['game_type']
        location_name=request.POST['location_name']
        location_url=request.POST['location_url']
        open_time=request.POST['open_time']
        close_time=request.POST['close_time']
        discription=request.POST['discription']
        image=request.FILES['image']
        rent=request.POST['rent']

        turf=turf_table.objects.create(image=image,
                                       ownername=request.user,
                                       name=turf_name,
                                       game_type=game_type,
                                       location=location_name,
                                       location_url=location_url,
                                       open_time=open_time,
                                       close_time=close_time,
                                       rent=rent,
                                       discription=discription,
                                       )
        turf.save()
        return redirect('ownersearchturf')
    return render (request,'addturf.html')

def deleteTurf(request,id):
    turf=turf_table.objects.get(id=id)
    turf.delete()
    return redirect('ownersearchturf')


def editTurf(request, id):
    
    data = get_object_or_404(turf_table, id=id)
    
    otime = str(data.open_time)
    ctime = str(data.close_time)
    description = data.discription
    
    if request.method == 'POST':
        form = turfForm(request.POST, request.FILES, instance=data)
        
        if form.is_valid():
            form.save()
            return redirect('ownersearchturf')  
        else:
            
            print("Form Errors:", form.errors)
    else:
        
        form = turfForm(instance=data)
    
    return render(request, 'editTurf.html', {
        'id': id,
        'form': form,  
        'otime': otime,
        'ctime': ctime,
        'disc': description,
    })
from datetime import datetime, timedelta

def delete_slots(turf):

    # Set the turf status to closed and slots to False
    turf.closed = True
    turf.slots = False
    turf.save()

    # Update expired field for all related BookingSlot objects in one query
    BookingSlot.objects.filter(turf=turf, expired=False).all().update(expired=True)



def create_new_slots(turf):
    slots = []
    
    # Initialize the start_time (e.g., 09:00 AM today)
    start_time = datetime.combine(datetime.today(), datetime.strptime("09:00", "%H:%M").time())
    
    # Generate 12 hourly slots
    for i in range(12):
        end_time = start_time + timedelta(hours=1)
        
        # Check if the slot is available or overdue
        status = "available" if start_time > datetime.now() else "overdued"
        
        # Convert start_time and end_time to 12-hour format (AM/PM)
        slots.append({
            "start_time": start_time.strftime("%I:%M %p"),  # 12-hour format with AM/PM
            "end_time": end_time.strftime("%I:%M %p"), 
            'user':None,   
            'played':False,  # 12-hour format with AM/PM
            "status": status
        })
        
        # Move to the next slot
        start_time = end_time
    
    # Filter for available slots
    available_slots = [slot for slot in slots if slot["status"] == "available"]

    # Update turf object based on the availability of slots
    turf.slots = bool(available_slots)  # Convert the list of available slots to a boolean
    turf.closed = False 
    turf.slots=True # Ensure the turf is open if there are available slots
    turf.save()

    # Create a new BookingSlot object in the database
    BookingSlot.objects.create(turf=turf, slots=slots)



def changeslots(request, id):
    turf = get_object_or_404(turf_table, id=id)

    # Ensure only the owner can modify slots
    if turf.ownername != request.user:
        return redirect('unauthorized_page')  # Redirect if unauthorized

    # If the turf is open, create new slots
    if turf.closed:
        create_new_slots(turf)
    else:
        # If the turf is closed, delete all slots
        delete_slots(turf)

    return redirect('ownersearchturf')


from datetime import datetime

def addreview(request,id):
    if request.method=="POST":
        name=request.POST['name']
        email=request.POST['email']
        msg=request.POST['msg']
        t=turf_table.objects.get(id=id)
        r_inst=reviewtable.objects.create(name=name,email=email,message=msg,turf=t)
        r_inst.save()
        rdata=reviewtable.objects.filter(turf=t)
        

    current_time = timezone.now().time()  # Get current time


        # Get the booking slot for the turf if not expired
    booking_slot = BookingSlot.objects.filter(turf=t, expired=False).first()
    
    if booking_slot and booking_slot.slots:
        all_booked = all(slot['status'] != 'available' for slot in booking_slot.slots)  # True if no slot is available
        all_slots_unavailable = not any(slot['status'] == 'available' for slot in booking_slot.slots)
          # True if all unavailable
    else:
        all_booked = True
        all_slots_unavailable = True

    if(all_slots_unavailable):
        t.slots=False
        t.save()  
        
    context = {
        'turf': t,
        'booking_slot': booking_slot,
        'slots': booking_slot.slots if booking_slot else None,  # Pass slots or None
        'current_time': current_time,
        'all_slots_unavailable': all_slots_unavailable,  # Flag for no available slots
        'all_booked': all_booked,
        'rdata':rdata  # Flag for all slots booked
    }
    

    return render(request, 'turfdetails.html', context)
   

def turfbookings(request,id):
    turf=turf_table.objects.get(id=id)
    turfbookings=BookingSlot.objects.filter(turf=turf,expired=False).first()

    # for booking in turfbookings:
    #     if isinstance(booking.booking_date, time):  # Fix the type check
    turfbookings.booking_date = datetime.combine(date.today(), turfbookings.booking_date)
    print(turfbookings.booking_date)
    return render (request,'turfbookings.html',{'turfbookings':turfbookings})

from datetime import datetime, date,time

def allbookings(request):
    allbookings=BookingSlot.objects.filter(turf__ownername=request.user).all()

    for booking in allbookings:
        if isinstance(booking.booking_date, time):  # Fix the type check
            booking.booking_date = datetime.combine(date.today(), booking.booking_date)
            
    return render (request,'allbookings.html',{'allbookings':allbookings})


def playedstatus(request, start_time, bid, user_id):
    try:
        # Fetch the booking slot by ID
        booking = BookingSlot.objects.get(id=bid)

        # Fetch all user bookings for the specified user and turf
        userbookings = UserBookingTable.objects.filter(
            turfname=booking.turf, customer__username=user_id
        ).all()

        # Track if all slots are expired
        all_slots_expired = True

        for userbooking in userbookings:
            updated = False  # Flag to check if any slot was updated

            for slot in userbooking.slots:
                if slot['start_time'] == start_time:
                    # Mark the specific slot as expired
                    slot['expired'] = True
                    updated = True

            if updated:
                userbooking.slots = userbooking.slots  # Update in memory
                userbooking.save()  # Save changes to the database

            # Recheck if all slots are expired after marking
            for slot in userbooking.slots:
                if not slot.get('expired', False):  # Any slot not expired
                    all_slots_expired = False
                    break  # Exit loop as soon as one non-expired slot is found

            if not all_slots_expired:
                break  # Exit outer loop if any slot remains active

        # Handle the case where all slots are expired
        if all_slots_expired:
            for userbooking in userbookings:
                userbooking.expired = True  # Mark user booking as expired
                userbooking.save()

        # Mark the specific slot as "played" in the main booking
        for slot in booking.slots:
            if slot.get('user') == user_id and slot['start_time'] == start_time:
                slot['played'] = True

        # Save the changes to the main booking
        booking.save()

        # Fetch all bookings to display
        all_bookings = BookingSlot.objects.filter(turf__ownername=request.user).all()

        return render(request, 'allbookings.html', {'allbookings': all_bookings})

    except BookingSlot.DoesNotExist:
        return render(request, 'error.html', {'message': 'Booking not found.'})
    except Exception as e:
        return render(request, 'error.html', {'message': str(e)})


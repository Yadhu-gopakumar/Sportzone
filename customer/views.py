from django.utils import timezone
from django.shortcuts import render,get_object_or_404
from turfowner.models import turf_table
from booking.models import BookingSlotTable as  BookingSlot,UserBookingTable
from django.contrib.auth.decorators import login_required


# Create your views here.
login_required(login_url='userlogin')
def userhome(request):
    
    latest_turfs = turf_table.objects.all().order_by('-id')[:3]

    return render(request,'index.html',{'latest_turfs':latest_turfs})

login_required(login_url='userlogin')
def viewturflist(request):
    turfs = turf_table.objects.all()
    return render(request, 'viewturflist.html', {'turfs': turfs})

login_required(login_url='userlogin')
def searchturf(request):
   
    if 'query' in request.GET:
        q=request.GET['query']
        res=turf_table.objects.filter(name__icontains=q) | turf_table.objects.filter(location__icontains=q) 
   
        if res is not None:
            context={
                'turfs':res,
                    }
        else:
            context={
            'turfs':res,
                }  
        return render(request,'viewturflist.html',context)
    


@login_required

def available_slots(request, turf_id):
    turf = get_object_or_404(turf_table, id=turf_id)
    current_time = timezone.now().time()  # Get current time

    try:
        # Get the booking slot for the turf if not expired
        booking_slot = BookingSlot.objects.filter(turf=turf, expired=False).first()
        
        if booking_slot and booking_slot.slots:
            all_booked = all(slot['status'] != 'available' for slot in booking_slot.slots)  # True if no slot is available
            all_slots_unavailable = not any(slot['status'] == 'available' for slot in booking_slot.slots)
              # True if all unavailable
        else:
            all_booked = True
            all_slots_unavailable = True

        if(all_slots_unavailable):

            turf.slots=False
            turf.save()  
           
    
            
        context = {
            'turf': turf,
            'booking_slot': booking_slot,
            'slots': booking_slot.slots if booking_slot else None,  # Pass slots or None
            'current_time': current_time,
            'all_slots_unavailable': all_slots_unavailable,  # Flag for no available slots
            'all_booked': all_booked,  # Flag for all slots booked
        }
    except BookingSlot.DoesNotExist:
        context = {
            'turf': turf,
            'slots': None, 
            'all_slots_unavailable': True,  # Set the flag to True if no slots exist
            'all_booked': True,  # If no slots exist, assume all are booked
        }

    return render(request, 'turfdetails.html', context)


from django.http import HttpResponse
from weasyprint import HTML
from django.template.loader import render_to_string

def download_ticket(request, booking_id):
    # Fetch booking details
    booking = UserBookingTable.objects.get(id=booking_id)
    turf = turf_table.objects.get(name=booking.turfname.name)
    image_url = turf.image.url
    context = {
        'booking': booking,
        'date': booking.booking_date,
        'user': booking.name,
        'turf_name': booking.turfname,
        'price': booking.amount,
        'image':image_url
    }
    
    # Render the ticket template to HTML
    html_string = render_to_string('ticket_template.html', context)

    # Define custom ticket size (in mm for example)
    ticket_size = (105, 148)  # A6 size (in mm) or custom size (width x height)

    # Convert the HTML string to PDF with custom size
    pdf = HTML(string=html_string).write_pdf(stylesheets=None, presentational_hints=True, 
                                              size=ticket_size)  # Specify size here

    # Create the HTTP response with the PDF file as content
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="ticket_{booking_id}.pdf"'

    return response


 
def userbookings(request):
    pass 


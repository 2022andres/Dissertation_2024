from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
import qrcode
from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from .models import Stadium,Events,SeatType,Booking,Fixtures,Athletics
from .forms import StadiumForm,EventsForm,SeatTypeForm,BookingForm,FixturesForm,AthleticsForm
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.db.models import Sum




# Create your views here.

def index(request):
    front_booking = Booking.objects.all()
    front_seat = SeatType.objects.all()
    form = BookingForm(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            booking = form.save(commit=False)  # Create a booking instance but don't save it to the database yet

            # Check if there are enough remaining seats for the selected seat type
            remaining_quantity = booking.seat_type.remaining_quantity
            if booking.number_of_tickets <= remaining_quantity:
                booking.save()  # Save the booking to the database
                # messages.success(request, "Your are now a valid customer")
                return redirect('viewbooking')
            else:
                messages.error(request, "Not enough seats available for this seat type.")
    else:
        form = BookingForm()
        
    fixture = Fixtures.objects.all()
    context ={
        'fixture':fixture,
        'front_seat':front_seat,
        'front_booking':front_booking,
        'form':form,
    }
    return render(request, 'ticket/index.html',context)

@login_required(login_url='login')
def stadium(request):
    return render(request, 'ticket/stadium.html',{})

@login_required(login_url='login')
def soccer(request):
    front_booking = Booking.objects.all()
    front_seat = SeatType.objects.all()
    form = BookingForm(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            booking = form.save(commit=False)  # Create a booking instance but don't save it to the database yet

            # Check if there are enough remaining seats for the selected seat type
            remaining_quantity = booking.seat_type.remaining_quantity
            if booking.number_of_tickets <= remaining_quantity:
                booking.save()  # Save the booking to the database
                # messages.success(request, "Your are now a valid customer")
                return redirect('viewbooking')
            else:
                messages.error(request, "Not enough seats available for this seat type.")
    else:
        form = BookingForm()
        
    fixture = Fixtures.objects.all()
    context ={
        'fixture':fixture,
        'front_seat':front_seat,
        'front_booking':front_booking,
        'form':form,
    }
    return render(request, 'ticket/soccer.html',context)

def viewbooking(request):
    user = request.user
    user_bookings = Booking.objects.filter(username=user)
    
    context = {
        'user_bookings': user_bookings,
    }
    return render(request, 'ticket/viewbooking.html', context)

def see_viewbooking(request, pk):
    viewbook = Booking.objects.get(id=pk)
    return render(request, 'ticket/viewbooking.html', {'viewbook': viewbook})

@login_required(login_url='login')
def athletics(request):
    return render(request, 'ticket/athletics.html',{})

@login_required(login_url='login')
def admin1(request):
    count_stadium = Stadium.objects.all().count()
    count_event = Events.objects.all().count()
    count_users = User.objects.all().count()
    total_booking_amount = Booking.objects.aggregate(Sum('total_cost'))['total_cost__sum'] or 0
    count_bookings = Booking.objects.all().count()

    context = {
        'count_stadium': count_stadium,
        'count_event': count_event,
        'count_users': count_users,
        'total_booking_amount': total_booking_amount,
        'count_bookings': count_bookings,
    }

    return render(request, 'ticket/admin1.html', context)


# ==========================STADIUM==========================
def stadiums(request):
    stadium = Stadium.objects.all()
    if request.method == 'POST':
        form = StadiumForm(request.POST,request.FILES)
        if form.is_valid():
            stadium = form.cleaned_data['stadium']

            # Check if a faculty with the same name already exists
            if Stadium.objects.filter(stadium=stadium).exists():
                messages.error(request, f"'{stadium}' already exists!")
                return redirect('stadiums')  # Redirect back to the faculty page without saving the form

            form.save()
            messages.success(request, "Stadium has been added!")
            return redirect('stadiums')

    else:
        form = StadiumForm()

    return render(request, 'ticket/stadiums.html', {'stadium': stadium, 'form': form})

def edit_stadiums(request, pk):
    editstad = Stadium.objects.get(id=pk)
    if request.method == 'POST':
        form = StadiumForm(request.POST, instance = editstad)
        if form.is_valid():
            form.save()
            messages.success(request, "Stadium updated successfully!")
            return redirect('stadiums')
    else:
        form = StadiumForm(instance = editstad)

    return render(request, 'ticket/edit_stadiums.html',{'form':form})

def delete_stadiums(request, pk):
    del_sta = Stadium.objects.get(id=pk)
    if request.method == 'POST':
        del_sta.delete()
        messages.success(request, "Stadium removed successfully! ")
        return redirect('stadiums')
    return render(request, 'ticket/delete_stadiums.html',{})

# ==========================END OF STADIUM==========================


# ======================EVENTS============================
def events(request):
    event = Events.objects.all()
    if request.method == 'POST':
        form = EventsForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Events has been added!")
            return redirect('events')
    else:
        form = EventsForm()

    return render(request, 'ticket/events.html', {'event': event, 'form': form})

def edit_events(request, pk):
    editevent = Events.objects.get(id=pk)
    if request.method == 'POST':
        form = EventsForm(request.POST, instance = editevent)
        if form.is_valid():
            form.save()
            messages.success(request, "Events updated successfully!")
            return redirect('events')
    else:
        form = EventsForm(instance = editevent)

    return render(request, 'ticket/edit_events.html',{'form':form})

def delete_events(request, pk):
    del_event = Events.objects.get(id=pk)
    if request.method == 'POST':
        del_event.delete()
        messages.success(request, "Events removed successfully! ")
        return redirect('events')
    return render(request, 'ticket/delete_events.html',{})

# ****************VIEW LEVEL******************
def view_events(request, pk):
    viewevent = Events.objects.get(id=pk)
    return render(request, 'ticket/view_events.html', {'viewevent': viewevent})


# ===============GAMES======================
def games(request):
    game = Games.objects.all()
    if request.method == 'POST':
        form = GamesForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Game added successfully")
            return redirect('games')
    else:
        form = GamesForm()
    return render(request, 'ticket/games.html', {'game': game, 'form': form})

def edit_game(request, pk):
    editgame = Games.objects.get(id=pk)
    if request.method == 'POST':
        form = GamesForm(request.POST, instance = editgame)
        if form.is_valid():
            form.save()
            messages.success(request, "Game updated successfully!")
            return redirect('games')
    else:
        form = GamesForm(instance = editgame)
    return render(request, 'ticket/edit_game.html',{'form':form})

def delete_game(request, pk):
    del_event = Games.objects.get(id=pk)
    if request.method == 'POST':
        del_event.delete()
        messages.success(request, "Game removed successfully! ")
        return redirect('games')
    return render(request, 'ticket/delete_game.html',{})

def view_game(request, pk):
    viewgame = Games.objects.get(id=pk)
    return render(request, 'ticket/view_game.html', {'viewgame': viewgame})


# ===============GAMES======================
def seat_type(request):
    seats = SeatType.objects.all()
    if request.method == 'POST':
        form = SeatTypeForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Seat added successfully")
            return redirect('seat_type')
    else:
        form = SeatTypeForm()
    return render(request, 'ticket/seat_type.html', {'seats': seats, 'form': form})

def edit_seat_type(request, pk):
    editgame = SeatType.objects.get(id=pk)
    if request.method == 'POST':
        form = SeatTypeForm(request.POST, instance = editgame)
        if form.is_valid():
            form.save()
            messages.success(request, "Seats updated successfully!")
            return redirect('seat_type')
    else:
        form = SeatTypeForm(instance = editgame)
    return render(request, 'ticket/edit_seat_type.html',{'form':form})

def delete_seat_type(request, pk):
    del_event = SeatType.objects.get(id=pk)
    if request.method == 'POST':
        del_event.delete()
        messages.success(request, "Seat removed successfully! ")
        return redirect('seat_type')
    return render(request, 'ticket/delete_seat_type.html',{})

def view_seat_type(request, pk):
    viewseat = SeatType.objects.get(id=pk)
    return render(request, 'ticket/view_seat_type.html', {'viewseat': viewseat})


# ===============BOOKINGS======================
def booking(request):
    book = Booking.objects.all()
    total_amount = Booking.objects.aggregate(Sum('total_cost'))['total_cost__sum']
    
    if request.method == 'POST':
        form = BookingForm(request.POST, request.FILES)
        if form.is_valid():
            booking = form.save(commit=False)
            remaining_quantity = booking.seat_type.remaining_quantity
            
            if booking.number_of_tickets <= remaining_quantity:
                booking.save()
                messages.success(request, "Booking added successfully")
                return redirect('viewbooking')
            else:
                messages.error(request, "Not enough seats available for this seat type.")
    else:
        form = BookingForm()
    
    return render(request, 'ticket/booking.html', {'book': book, 'form': form, 'total_amount': total_amount})

def edit_booking(request, pk):
    editbook = Booking.objects.get(id=pk)
    if request.method == 'POST':
        form = BookingForm(request.POST, instance = editbook)
        if form.is_valid():
            form.save()
            messages.success(request, "Booking updated successfully!")
            return redirect('booking')
    else:
        form = BookingForm(instance = editbook)
    return render(request, 'ticket/edit_booking.html',{'form':form})

def delete_booking(request, pk):
    del_book = Booking.objects.get(id=pk)
    if request.method == 'POST':
        del_book.delete()
        messages.success(request, "Booking removed successfully! ")
        return redirect('booking')
    return render(request, 'ticket/delete_booking.html',{})

def view_booking(request, pk):
    viewbook = Booking.objects.get(id=pk)
    return render(request, 'ticket/view_booking.html', {'viewbook': viewbook})

def del_front_booking(request, pk):
    del_book = Booking.objects.get(id=pk)
    if request.method == 'POST':
        # Check if the QR code has been scanned
        if del_book.qr_scanned:
            messages.error(request, "This ticket has already been scanned. You cannot cancel it.")
        else:
            del_book.delete()
            messages.success(request, "Booking successfully canceled.")
        return redirect('soccer')
    return render(request, 'ticket/del_front_booking.html', {})



# ===============FIXTURES======================
def fixtures(request):
    fixture = Fixtures.objects.all()
    if request.method == 'POST':
        form = FixturesForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Seat added successfully")
            return redirect('fixtures')
    else:
        form = FixturesForm()
    return render(request, 'ticket/fixtures.html', {'fixture': fixture, 'form': form})

def edit_fixtures(request, pk):
    editfixture = Fixtures.objects.get(id=pk)
    if request.method == 'POST':
        form = FixturesForm(request.POST, instance = editfixture)
        if form.is_valid():
            form.save()
            messages.success(request, "Fixtures updated successfully!")
            return redirect('fixtures')
    else:
        form = FixturesForm(instance = editfixture)
    return render(request, 'ticket/edit_fixtures.html',{'form':form})

def delete_fixtures(request, pk):
    del_fixture = Fixtures.objects.get(id=pk)
    if request.method == 'POST':
        del_fixture.delete()
        messages.success(request, "Booking removed successfully! ")
        return redirect('fixtures')
    return render(request, 'ticket/delete_fixtures.html',{})

def view_fixtures(request, pk):
    viewfixture = Fixtures.objects.get(id=pk)
    return render(request, 'ticket/view_fixtures.html', {'viewfixture': viewfixture})



# ===============ATHLETICS EVENT======================
def athletics_event(request):
    athletics_fixture = Athletics.objects.all()
    if request.method == 'POST':
        form = AthleticsForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Athletics Event added successfully")
            return redirect('athletics_event')
    else:
        form = AthleticsForm()
    return render(request, 'ticket/athletics_event.html', {'athletics_fixture': athletics_fixture, 'form': form})

def delete_athletics_event(request, pk):
    del_event = Athletics.objects.get(id=pk)
    if request.method == 'POST':
        del_event.delete()
        messages.success(request, "Event removed successfully! ")
        return redirect('athletics_event')
    return render(request, 'ticket/delete_athletics_event.html',{})

def edit_athletics_event(request, pk):
    editevent = Athletics.objects.get(id=pk)
    if request.method == 'POST':
        form = AthleticsForm(request.POST, instance = editevent)
        if form.is_valid():
            form.save()
            messages.success(request, "Athletics Events updated successfully!")
            return redirect('athletics_event')
    else:
        form = AthleticsForm(instance = editevent)
    return render(request, 'ticket/edit_athletics_event.html',{'form':form})

def view_athletics_event(request, pk):
    viewevent = Athletics.objects.get(id=pk)
    return render(request, 'ticket/view_athletics_event.html', {'viewevent': viewevent})

# ===============FIXTURES PAGE======================
def fixtures_page(request):
    front_seat = SeatType.objects.all()
    front_booking = Booking.objects.all()
    form = BookingForm(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            booking = form.save(commit=False)  # Create a booking instance but don't save it to the database yet

            # Check if there are enough remaining seats for the selected seat type
            remaining_quantity = booking.seat_type.remaining_quantity
            if booking.number_of_tickets <= remaining_quantity:
                booking.save()  # Save the booking to the database
                # messages.success(request, "Your are now a valid customer")
                return redirect('viewbooking')
            else:
                messages.error(request, "No ticket are available for this match.")
    else:
        form = BookingForm()
        
    fixture = Fixtures.objects.all()
    context ={
        'fixture':fixture,
        'front_seat':front_seat,
        'front_booking':front_booking,
        'form':form,
    }
    return render(request, 'ticket/fixtures_page.html', context)

# ===============END FIXTURES======================
def update_button_state(request):
    button_state = request.POST.get('button_state', 'false')
    request.session['button_state'] = button_state.lower() == 'true'
    return JsonResponse({'success': True})


# ===============USERS======================
def users(request):
    users = User.objects.all()
    return render(request, 'ticket/users.html', {'users': users})

def delete_users(request, pk):
    del_user = User.objects.get(id=pk)
    if request.method == 'POST':
        del_user.delete()
        messages.success(request, "User removed successfully! ")
        return redirect('users')
    return render(request, 'ticket/delete_users.html',{})




# ================================QR CODE=============================

def generate_qr_code(request, booking_id):
    # Retrieve the booking data from the database
    booking = Booking.objects.get(id=booking_id)

    # Check if the scan limit has been reached
    if booking.scan_count >= 2:
        return HttpResponse('<h1 style="font-size:60px; color: red; margin-left: 200px; margin-top: 300px;">You have exceeded the scan limit.<h1>')

    # Create a QR code with the booking details
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(f"This is the Ticket Booking Details:\n\nFixtures: {booking.teamfixture}\n\nCustomer: {booking.username}\n\nAddress: {booking.address}\n\nContact: {booking.contact}\n\nEvent: {booking.event}\n\nGame Date: {booking.teamfixture.game_date}\nGame Time: {booking.teamfixture.game_time}\n\nNumber of Tickets: {booking.number_of_tickets}\n\nSeat Type: {booking.seat_type}\n\nNumber of Tickets: {booking.number_of_tickets}\n\nPrice of Seat Type: Nle{booking.seat_type.seat_price}\n\nTotal Amount to pay: Nle{booking.total_cost}")
    qr.make(fit=True)

    # Update the scan count
    booking.scan_count += 1
    booking.save()

    # Create an HTTP response to display the QR code
    response = HttpResponse(content_type='image/png')
    img = qr.make_image(fill_color="black", back_color="white")
    img.save(response, "PNG")

    return response

def payment(request):
    user = request.user
    user_bookings = Booking.objects.filter(username=user)
    
    context = {
        'user_bookings': user_bookings,
    }
    return render(request, 'ticket/payment.html',context)

def check_qr_status(request):
    booking_id = request.GET.get('booking_id')
    booking = Booking.objects.get(id=booking_id)
    qr_scanned = booking.qr_scanned
    return JsonResponse({'qr_scanned': qr_scanned})

def booknow(request):
    front_seat = SeatType.objects.all()
    front_booking = Booking.objects.all()
    form = BookingForm(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            booking = form.save(commit=False)  # Create a booking instance but don't save it to the database yet
            # Check if there are enough remaining seats for the selected seat type
            remaining_quantity = booking.seat_type.remaining_quantity
            if booking.number_of_tickets <= remaining_quantity:
                booking.save()  # Save the booking to the database
                # messages.success(request, "Your are now a valid customer")
                return redirect('viewbooking')
            else:
                messages.error(request, "Not Enough tickets are available for this match.The number\n of tickets you entered, exceed the amount of tickets available")
    else:
        form = BookingForm()
        
    fixture = Fixtures.objects.all()
    context ={
        'fixture':fixture,
        'front_seat':front_seat,
        'front_booking':front_booking,
        'form':form,
    }
    return render(request, 'ticket/booknow.html', context)

# ===============FIXTURES======================
def homefixtures(request):cdstadium
    fixture = Fixtures.objects.all()
    if request.method == 'POST':
        form = FixturesForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Seat added successfully")
            return redirect('index')
    else:
        form = FixturesForm()
    return render(request, 'ticket/fixtures.html', {'fixture': fixture, 'form': form})
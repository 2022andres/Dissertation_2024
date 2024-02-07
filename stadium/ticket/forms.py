from django import forms
from django.forms import ModelForm
from .models import Stadium,Events,SeatType,Booking,Fixtures,Athletics


class StadiumForm(forms.ModelForm):
    class Meta:
        model = Stadium
        fields = ['stadium','location','stadium_image']
        labels = {
            'stadium_image':'',
        }
        widgets = {
            'stadium': forms.TextInput(attrs={'class':'form-control shadow-none'}),
            'location': forms.TextInput(attrs={'class':'form-control shadow-none mb-3'}),
        }

class EventsForm(forms.ModelForm):
    class Meta:
        model = Events
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class':'form-control shadow-none'}),
            
        }

class SeatTypeForm(forms.ModelForm):
    class Meta:
        model = SeatType
        fields = ['seat_type','available_quantity','seat_price']
        widgets = {
            'seat_type':forms.Select(attrs={'class':'form-control shadow-none mb-3'}),
            'available_quantity':forms.TextInput(attrs={'class':'form-control shadow-none mb-3'}),
            'seat_price':forms.TextInput(attrs={'class':'form-control shadow-none mb-3'}),
        }

class FixturesForm(forms.ModelForm):
    class Meta:
        model = Fixtures
        fields = ['team1','team2','game_date','game_time','venue','description','team1_image','team2_image']
        widgets = {
            'team1':forms.TextInput(attrs={'class':'form-control shadow-none mb-3'}),
            'team2':forms.TextInput(attrs={'class':'form-control shadow-none mb-3'}),
            'game_date':forms.DateInput(attrs={'class':'form-control shadow-none mb-3'}),
            'game_time':forms.TimeInput(attrs={'class':'form-control shadow-none mb-3'}),
            'description':forms.TextInput(attrs={'class':'form-control shadow-none mb-3'}),
            'venue':forms.Select(attrs={'class':'form-control shadow-none mb-3'}),
            
        }

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['username','address','contact','event','seat_type','number_of_tickets','teamfixture']
        exclude = ['total_cost']
        widgets = {
            'username':forms.Select(attrs={'class':'form-control shadow-none mb-3'}),
            'address':forms.TextInput(attrs={'class':'form-control shadow-none mb-3'}),
            'contact':forms.TextInput(attrs={'class':'form-control shadow-none mb-3'}),
            'event':forms.Select(attrs={'class':'form-control shadow-none mb-3'}),
            'seat_type':forms.Select(attrs={'class':'form-control shadow-none mb-3'}),
            'number_of_tickets':forms.TextInput(attrs={'class':'form-control shadow-none mb-3',
            'oninput': "validateBookingInput(this);"}),
            'teamfixture':forms.Select(attrs={'class':'form-control shadow-none mb-3'}),
        }

class AthleticsForm(forms.ModelForm):
    class Meta:
        model = Athletics
        fields = ['title','event_date','event_time','description','venue','event_image']
        # labels = {
        #     'stadium_image':'',
        # }
        widgets = {
            'title': forms.TextInput(attrs={'class':'form-control shadow-none'}),
            'event_date': forms.DateInput(attrs={'class':'form-control shadow-none mb-3'}),
            'event_time': forms.DateInput(attrs={'class':'form-control shadow-none mb-3'}),
            'description': forms.DateInput(attrs={'class':'form-control shadow-none mb-3'}),
            'venue': forms.Select(attrs={'class':'form-control shadow-none mb-3'}),
            
        }


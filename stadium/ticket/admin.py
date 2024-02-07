from django.contrib import admin
from .models import Stadium,Events,SeatType,Booking
# Register your models here.
admin.site.register(Stadium)
admin.site.register(Events)
admin.site.register(SeatType)
admin.site.register(Booking)
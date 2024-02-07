from django.db import models
from django.contrib.auth.models import User
# Create your models here.
TICKET_CATEGORY = (
        ('VIP','VIP'),
        ('Local','Local'),
        ('Open Stand','Open Stand'),
)

class Stadium(models.Model):
    stadium = models.CharField(max_length=100, null=True)
    location = models.CharField(max_length=100)
    stadium_image = models.ImageField(null=True, blank=True, upload_to='Profile_Images')
    def __str__(self):
        return self.stadium
    
class Events(models.Model):
    name = models.CharField(max_length=100,null=True)
    def __str__(self):
        return self.name

class Fixtures(models.Model):
    team1 = models.CharField(max_length=100, null=True)
    team2 = models.CharField(max_length=100, null=True)
    game_date = models.DateField()
    game_time = models.TimeField()
    description = models.TextField(max_length=200)
    venue = models.ForeignKey(Stadium,on_delete=models.CASCADE)
    team1_image = models.ImageField(null=True, blank=True, upload_to='Profile_Images/')
    team2_image = models.ImageField(null=True, blank=True, upload_to='Profile_Images/')
    def __str__(self):
        return f" {self.team1} vs {self.team2}"

class Athletics(models.Model):
    title = models.CharField(max_length=100, null=True)
    event_date = models.DateField()
    event_time = models.TimeField()
    description = models.TextField(max_length=200)
    venue = models.ForeignKey(Stadium,on_delete=models.CASCADE)
    event_image = models.ImageField(null=True, blank=True, upload_to='Profile_Images/')
    def __str__(self):
        return f" {self.title} event at {self.venue}"   
    
class SeatType(models.Model):
    CHOICES = [
        ('VIP', 'VIP'),
        ('Local Seat', 'Local Seat'),
        ('Open Stand', 'Open Stand'),
    ]

    seat_type = models.CharField(max_length=20, choices=CHOICES)
    available_quantity = models.IntegerField()  # Initial quantity of items
    seat_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    @property
    def remaining_quantity(self):
        used_quantity = self.booking_set.aggregate(total_used=models.Sum('number_of_tickets'))['total_used']
        if used_quantity is None:
            used_quantity = 0
        return self.available_quantity - used_quantity

    def __str__(self):
        return self.seat_type

class Booking(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=100, null=True)
    contact = models.IntegerField()
    event = models.ForeignKey(Events, on_delete=models.CASCADE)
    teamfixture = models.ForeignKey(Fixtures, on_delete=models.CASCADE)
    seat_type = models.ForeignKey(SeatType, on_delete=models.CASCADE)
    number_of_tickets = models.IntegerField()
    scan_count = models.PositiveIntegerField(default=0)
    total_cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    qr_scanned = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.username.username} - {self.event} - {self.teamfixture}"
    
    def save(self, *args, **kwargs):
        if self.seat_type and self.number_of_tickets:
            if self.number_of_tickets > 0 and self.number_of_tickets <= self.seat_type.remaining_quantity:
                # Calculate the total cost
                self.total_cost = self.seat_type.seat_price * self.number_of_tickets
                super(Booking, self).save(*args, **kwargs)
            else:
                # Handle cases where not enough tickets are available
                # You can raise an exception or return an error message here.
                self.total_cost = 0  # Set total_cost to 0 if there are not enough tickets.
                super(Booking, self).save(*args, **kwargs)















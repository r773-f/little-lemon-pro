from django.db import models

# Create your models here.
class Booking(models.Model):
    name = models.CharField (max_length=100)
    number_of_guest = models.IntegerField(null=True)
    booking_date = models.DateTimeField(null=True)

class Menu(models.Model):
    title = models.CharField(max_length=255)
    price = models.DecimalField(max_digits = 10, decimal_places = 2)
    inventory = models.IntegerField()
    def str(self):
        return f'{self.title} : {str(self.price)}'
    

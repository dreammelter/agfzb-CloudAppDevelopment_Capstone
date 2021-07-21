from os import name
from django.db import models
from django.db.models.fields.related import ManyToManyField
from django.utils.timezone import now



class CarMake(models.Model):
    name = models.CharField(max_length=25, null=False, default='Car Make')
    description = models.CharField(max_length=500, default="Description of car make or manufacturer.")

    def __str__(self):
        return "Make: " + self.name + " - " + self.description


# <HINT> Create a Car Model model `class CarModel(models.Model):`:
# - __str__ method to print a car make object
class CarModel(models.Model):
    car_make = models.ManyToManyField(CarMake)
    name = models.CharField(null=False, max_length=25)
    dealership = models.IntegerField(null=False, default=0) # dealer id is "dealership" in the db.

    # define choices for car type
    SEDAN = 'sedan'
    SUV = 'suv'
    WAGON = 'wagon'
    COUPE = 'coupe'
    HATCH = 'hatchback'
    CONVERT = 'convertible'
    VANS = 'vans'
    SPORTS = 'sports'
    MUSCLE = 'muscle'
    SUPER = 'super'
    ELECTRIC = 'electric'
    LIMO = 'limo'
    CAR_TYPE_CHOICES = [
        (SEDAN, 'Sedan'),
        (SUV, 'SUV'),
        (WAGON, 'Station Wagon'),
        (COUPE, 'Coupe'),
        (HATCH, 'Hatchback'),
        (CONVERT, 'Convertible'),
        (VANS, 'Van / Minivan'),
        (SPORTS, 'Sports Car'),
        (MUSCLE, 'Muscle Car'),
        (SUPER, 'Super Car'),
        (ELECTRIC, 'Electric Car'),
        (LIMO, 'Limousine')
    ]
    car_type = models.CharField(
        max_length = 15,
        choices = CAR_TYPE_CHOICES,
        default = COUPE
    )
    car_year = models.DateField() # downside to DateField is it looks for the full date...

    def __str__(self) -> str:
        return self.name + " " + self.car_year + " - " + self.car_type


# <HINT> Create a plain Python class `CarDealer` to hold dealer data


# <HINT> Create a plain Python class `DealerReview` to hold review data

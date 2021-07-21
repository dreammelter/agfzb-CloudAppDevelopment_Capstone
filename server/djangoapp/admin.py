from django.contrib import admin
from .models import CarMake, CarModel


# Register your models here.

class CarModelInline:
    model = CarModel


class CarModelAdmin:
    list_display = ['name']


class CarMakeAdmin:
    inlines = [CarModelInline]
    list_display = ('name', 'car_year')
    list_filter = ['car_type']
    search_fields = ['name','car_year','car_type']

# Register models here
admin.site.register(CarMake)
admin.site.register(CarModel)
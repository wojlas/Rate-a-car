from django.forms import ModelForm
import django.forms as forms
from rate_a_car_app.models import Car, Brand, Rate, CHOICES

class AddCarForm(ModelForm):
    class Meta:
        model = Car
        exclude = ['rate']

class AddBrandForm(ModelForm):
    class Meta:
        model = Brand
        fields ='__all__'

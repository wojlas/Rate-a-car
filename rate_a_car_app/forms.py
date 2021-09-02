import django.forms as forms
from django.contrib.auth.models import User
from django.forms import ModelForm

from .models import Brand, CarModel, CarOwners


class NewBrandForm(ModelForm):
    class Meta:
        model = Brand
        fields = '__all__'


class NewModelForm(ModelForm):
    class Meta:
        model = CarModel
        fields = ['brand', 'model', 'version', 'production_from', 'production_to']
        production_to = forms.IntegerField(label='Produkcja do', widget=forms.IntegerField)


class LoginForm(forms.Form):
    login = forms.CharField(max_length=32, label='Login')
    password = forms.CharField(widget=forms.PasswordInput, label='Hasło')

class AddCarsHistoryForm(ModelForm):
    class Meta:
        model = CarOwners
        fields = ['car','use_from', 'use_to']
        # use_to = forms.CharField(widget=forms.IntegerField, max_length=4)
        owner = forms.ModelChoiceField(widget=forms.IntegerField, queryset=User.objects.all())
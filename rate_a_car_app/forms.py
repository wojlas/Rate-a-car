import django.forms as forms
from django.forms import ModelForm

from .models import Brand, CarModel


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

from django.forms import ModelForm
import django.forms as forms
from .models import Brand, CarModel, Car


class NewBrandForm(ModelForm):
    class Meta:
        model = Brand
        fields = '__all__'

class NewModelForm(ModelForm):
    class Meta:
        model = CarModel
        fields = '__all__'


class LoginForm(forms.Form):
    login = forms.CharField(max_length=32, label='Login')
    password = forms.CharField(widget=forms.PasswordInput, label='Hasło')
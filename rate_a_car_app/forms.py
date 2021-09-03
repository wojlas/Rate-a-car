import django.forms as forms
from django.contrib.auth.models import User
from django.forms import ModelForm

from .models import Brand, CarModel, CarOwners, Profile


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

class ForgotPassForm(forms.Form):
    user = forms.CharField(label='Login', max_length=32)
    new_pass1 = forms.CharField(widget=forms.PasswordInput, label='Nowe hasło')
    new_pass2 = forms.CharField(widget=forms.PasswordInput, label='Powtórz hasło')

    # def clean(self):
    #     cleaned_data = super().clean()
    #     if cleaned_data.get('new_pass1') != cleaned_data.get('new_pass2'):
    #         raise forms.ValidationError("Hasła nie są takie same!")
    #     return cleaned_data

class RegisterUserForm(ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput, label='Hasło')
    password2 = forms.CharField(widget=forms.PasswordInput, label='Powtórz hasło')
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'email', 'first_name', 'last_name']

    def clean(self):
        cleaned_data = super(RegisterUserForm, self).clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 != password2:
            raise forms.ValidationError('Hasła muszą być identyczne')


class AddCarsHistoryForm(ModelForm):
    class Meta:
        model = CarOwners
        fields = ['car','use_from', 'use_to']
        # use_to = forms.CharField(widget=forms.IntegerField, max_length=4)
        owner = forms.ModelChoiceField(widget=forms.IntegerField, queryset=User.objects.all())
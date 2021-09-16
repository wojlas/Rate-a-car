import django.forms as forms
from django.contrib.auth.models import User
from django.forms import ModelForm

from .models import Brand, CarModel, CarOwners, Profile, Rate, Notice, Images


class NewBrandForm(ModelForm):
    """Create new brand, based on model Brand"""
    class Meta:
        model = Brand
        fields = '__all__'


class NewModelForm(ModelForm):
    """Create new model,
    select brand from list and type model informations"""

    class Meta:
        model = CarModel
        fields = ['brand', 'model', 'version', 'production_from', 'production_to']
        production_to = forms.IntegerField(label='Produkcja do', widget=forms.IntegerField)


class LoginForm(forms.Form):
    """Form for user login"""
    login = forms.CharField(max_length=32, label='Login')
    password = forms.CharField(widget=forms.PasswordInput, label='Hasło')

class ForgotPassForm(forms.Form):
    """Form for reset user password"""
    user = forms.CharField(label='Login', max_length=32)
    new_pass1 = forms.CharField(widget=forms.PasswordInput, label='Nowe hasło')
    new_pass2 = forms.CharField(widget=forms.PasswordInput, label='Powtórz hasło')

    # def clean(self):
    #     cleaned_data = super().clean()
    #     if cleaned_data.get('new_pass1') != cleaned_data.get('new_pass2'):
    #         raise forms.ValidationError("Hasła nie są takie same!")
    #     return cleaned_data

class RegisterUserForm(ModelForm):
    """Form for register new user"""
    password1 = forms.CharField(widget=forms.PasswordInput, label='Hasło')
    password2 = forms.CharField(widget=forms.PasswordInput, label='Powtórz hasło')
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'email', 'first_name', 'last_name']

    # def clean(self):
    #     cleaned_data = super(RegisterUserForm, self).clean()
    #     password1 = cleaned_data.get("password1")
    #     password2 = cleaned_data.get("password2")
    #
    #     if password1 != password2:
    #         raise forms.ValidationError('Hasła muszą być identyczne')


class AddCarsHistoryForm(ModelForm):
    """Form for add car to user history"""
    class Meta:
        model = CarOwners
        fields = ['car','use_from', 'use_to']
        # use_to = forms.CharField(widget=forms.IntegerField, max_length=4)
        owner = forms.ModelChoiceField(widget=forms.IntegerField, queryset=User.objects.all())

class RateForm(ModelForm):
    """Form for car voted"""
    class Meta:
        model = Rate
        exclude = ['carmodel', 'user']
        carmodel = forms.ModelChoiceField(widget=forms.HiddenInput, queryset=CarModel.objects.all())
        user = forms.ModelChoiceField(widget=forms.HiddenInput, queryset=User.objects.all())

class NoticeForm(ModelForm):
    class Meta:
        model = Notice
        exclude = ['date', 'author', 'car']
        author = forms.ModelChoiceField(widget=forms.HiddenInput, queryset=User.objects.all())
        car = forms.ModelChoiceField(widget=forms.HiddenInput, queryset=CarModel.objects.all())

class SettingsDataForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']

class SettingsChangePasswordForm(forms.Form):
    old_password = forms.CharField(widget=forms.PasswordInput, label='Podaj obecne hasło')
    password1 = forms.CharField(widget=forms.PasswordInput, label='Nowe hasło')
    password2 = forms.CharField(widget=forms.PasswordInput, label='Powtórz hasło')

    def clean(self):
        cleaned_data = super(SettingsChangePasswordForm, self).clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 != password2:
            raise forms.ValidationError('Hasła muszą być identyczne')

class UpdateAvatarForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['avatar']

class UploadCarPictureForm(ModelForm):
    class Meta:
        model = Images
        fields = ['image']
        carmodel = forms.ModelChoiceField(widget=forms.HiddenInput, queryset=CarModel.objects.all())
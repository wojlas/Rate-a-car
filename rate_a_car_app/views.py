import json
import random

from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User, Group
from django.core.paginator import Paginator
from django.core.serializers.json import DjangoJSONEncoder
from django.shortcuts import render, redirect
# Create your views here.
from django.views import View

from .forms import LoginForm, NewBrandForm, NewModelForm, AddCarsHistoryForm, ForgotPassForm, RegisterUserForm, \
    RateForm, NoticeForm, SettingsDataForm, SettingsChangePasswordForm, UpdateAvatarForm, UploadCarPictureForm
from .models import Brand, CarModel, Profile, CarOwners, Rate, Notice, Images


class IndexView(View):
    """Display aplications main page
    """

    def get(self, request):
        new_cars = CarModel.objects.order_by('-date')[:10]
        new_notices = Notice.objects.order_by('-date')[:10]
        new_rates = Rate.objects.order_by('-date')[:10]
        best_cars = CarModel.objects.order_by('-average_rate')[:10]
        images_query = list(Images.objects.all())
        cnt = {'new_cars': new_cars,
               'new_notices': new_notices,
               'new_rates': new_rates,
               'best_cars': best_cars,
               'random_images':random.sample(images_query, 3)}
        return render(request, 'rate_a_car_app/index.html', cnt)


class LoginView(View):
    """View used to login user"""

    def get(self, request):
        """Render form"""
        form = LoginForm()
        return render(request, 'rate_a_car_app/login.html', {'form': form})

    def post(self, request):
        """if user exist and password is correct user is logged in and redirect to main page"""
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['login'], password=form.cleaned_data['password'])
            if user is not None:
                login(request, user)
                return redirect('/')
            else:
                form = LoginForm()
                return render(request, 'rate_a_car_app/login.html', {'form': form, 'error': 'Zły login lub hasło'})


class LogoutView(View):
    """logout user"""

    def get(self, request):
        logout(request)
        return redirect('/')


class ForgotPassView(View):
    """View to reset password"""

    def get(self, request):
        """View render form with 3 inputs,
        username and 2 password input"""
        form = ForgotPassForm()
        return render(request, 'rate_a_car_app/new-password.html', {'form': form})

    def post(self, request):
        """Set password for user type in username field, if password fields isn't the same,
        user is informed about it"""
        form = ForgotPassForm(request.POST)
        if form.is_valid():
            if form.cleaned_data['new_pass1'] != form.cleaned_data['new_pass2']:
                form = ForgotPassForm()
                return render(request, 'rate_a_car_app/new-password.html',
                              {'form': form, 'error': 'Hasła muszą być identyczne'})
            else:
                user = User.objects.get(username=form.cleaned_data['user'])
                user.set_password(form.cleaned_data['new_pass1'])
                user.save()
                return redirect('/login/')
        else:
            form = ForgotPassForm()
            return render(request, 'rate_a_car_app/new-password.html', {'form': form, 'error': 'Somethings wrong'})


class RegisterView(View):
    """new user register"""

    def get(self, request):
        form_user = RegisterUserForm()
        return render(request, 'rate_a_car_app/register.html', {'form_user': form_user})

    def post(self, request):
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            if form.cleaned_data['password1'] == form.cleaned_data['password2']:
                user = User.objects.create_user(username=form.cleaned_data['username'],
                                           password=form.cleaned_data['password1'],
                                           first_name=form.cleaned_data['first_name'],
                                           last_name=form.cleaned_data['last_name'],
                                           email=form.cleaned_data['email'])
                Profile.objects.create(user=user)
                group = Group.objects.get(name='regular')
                group.user_set.add(user)
                return redirect('/login/')
            else:
                form_user = RegisterUserForm()
                return render(request, 'rate_a_car_app/register.html',
                              {'form_user': form_user, 'error': 'Hasła muszą być identyczne'})
        else:
            form_user = RegisterUserForm()
            return render(request, 'rate_a_car_app/register.html', {'form_user': form_user, 'error': 'Nazwa zajęta'})


class NewBrandView(View):
    """View adding new brand to database
    """

    def post(self, request):
        add_brand = NewBrandForm(request.POST)
        if add_brand.is_valid():
            Brand.objects.create(brand=add_brand.cleaned_data['brand'])
            return redirect('/create-model/')
        else:
            ctx = {
                'add_brand': NewBrandForm(),
                'error': 'Marka o tej nazwie już istnieje'
            }
            return redirect('/create-model/')


class NewModelView(LoginRequiredMixin, View):
    """Adding new car model with model name, version and years of production
    only for loged users"""
    login_url = '/login'
    redirect_field_name = 'new-model'

    def get(self, request):
        ctx = {'add_model': NewModelForm(),
               'add_brand': NewBrandForm()}
        return render(request, 'rate_a_car_app/create-model.html', ctx)

    def post(self, request):
        add_model = NewModelForm(request.POST)
        if add_model.is_valid():
            CarModel.objects.create(brand=add_model.cleaned_data['brand'],
                                    model=add_model.cleaned_data['model'],
                                    version=add_model.cleaned_data['version'],
                                    production_from=add_model.cleaned_data['production_from'],
                                    production_to=add_model.cleaned_data['production_to'])
            return redirect(f'/profile/history/{request.user.username}/')
        else:
            ctx = {'add_model': NewModelForm()}
            return render(request, 'rate_a_car_app/create-model.html', ctx)


class BrowseCarView(View):
    """Most important view in project

    User can browse a car filtering by brand and simply skip to car details"""

    def get(self, request):
        ctx = {'new_car': CarModel.objects.all().order_by('brand'),
               'brands': Brand.objects.all()}
        return render(request, 'rate_a_car_app/cars.html', ctx)


class BrowseBrandModelsView(View):
    """Based on BrowseCarView

    Car list filtering by brand"""

    def get(self, request, brand_name):
        brand = Brand.objects.get(brand=brand_name)
        ctx = {'cars': CarModel.objects.filter(brand=brand.id).order_by('model'),
               'brands': Brand.objects.all(),
               'brand_name': brand}
        return render(request, 'rate_a_car_app/brand-cars.html', ctx)


class CarDetailsView(View):
    """Car details

    Information about car, rates, notices"""

    def get(self, request, version, car):
        car = CarModel.objects.get(model=car, version=version)
        owners = CarOwners.objects.filter(car=car)
        notices = Notice.objects.filter(car=car)
        add_pic_form = UploadCarPictureForm(initial={'carmodel': car})

        if request.user in [own.owner.user for own in owners]:
            rate_form = RateForm(initial={'carmodel': car,
                                          'user': request.user})
            notice_form = NoticeForm(initial={'author': request.user,
                                              'car': car})
        else:
            rate_form = None
            notice_form = None

        rates = Rate.objects.filter(carmodel=car).order_by('-date')[:10]
        if len([rate.design for rate in rates]) > 0:
            division_by = len([rate.design for rate in rates])
        else:
            division_by = 1
        summary_design = round(sum([rate.design for rate in rates]) / division_by, 2)
        summary_endurance = round(sum([rate.endurance for rate in rates]) / division_by, 2)
        summary_cost = round(sum([rate.operation_cost for rate in rates]) / division_by, 2)
        summary_leading = round(sum([rate.leading for rate in rates]) / division_by, 2)
        average = (summary_leading + summary_cost + summary_design + summary_endurance) / 4
        car.average_rate = round(average, 2)
        car.save()
        ctx = {'car': car,
               'rate_form': rate_form,
               'notice_form': notice_form,
               'rates': rates,
               'notices': notices,
               'summary_design': summary_design,
               'summary_endurance': summary_endurance,
               'summary_cost': summary_cost,
               'summary_leading': summary_leading,
               'avarage': round(average,2),
               'num_of_opinions': notices.count(),
               'num_of_rates': rates.count(),
               'add_pic': add_pic_form,
               'images': Images.objects.filter(carmodel=car.id)}

        return render(request, 'rate_a_car_app/car-details.html', ctx)

    def post(self, request, car, version):
        car = CarModel.objects.get(model=car, version=version)
        if 'rates' in request.POST:
            form = RateForm(request.POST)
            if form.is_valid():
                Rate.objects.create(design=form.cleaned_data['design'],
                                    leading=form.cleaned_data['leading'],
                                    operation_cost=form.cleaned_data['operation_cost'],
                                    endurance=form.cleaned_data['endurance'],
                                    carmodel=car,
                                    user=request.user)
                return redirect(f"/cars/{car.model}/{version}/")
            else:
                car = CarModel.objects.get(model=car, version=version)
                owners = CarOwners.objects.filter(car=car)
                notices = Notice.objects.filter(car=car)
                add_pic_form = UploadCarPictureForm

                if request.user in [own.owner.user for own in owners]:
                    rate_form = RateForm(initial={'carmodel': car,
                                                  'user': request.user})
                    notice_form = NoticeForm(initial={'author': request.user,
                                                      'car': car})
                else:
                    rate_form = None
                    notice_form = None
                rates = Rate.objects.filter(carmodel=car).order_by('-date')[:10]
                if len([rate.design for rate in rates]) > 0:
                    division_by = len([rate.design for rate in rates])
                else:
                    division_by = 1
                summary_design = round(sum([rate.design for rate in rates]) / division_by, 2)
                summary_endurance = round(sum([rate.endurance for rate in rates]) / division_by, 2)
                summary_cost = round(sum([rate.operation_cost for rate in rates]) / division_by, 2)
                summary_leading = round(sum([rate.leading for rate in rates]) / division_by, 2)
                average = (summary_leading + summary_cost + summary_design + summary_endurance) / 4
                car.average_rate = round(average, 2)
                car.save()
                ctx = {'car': car,
                       'rate_form': rate_form,
                       'notice_form': notice_form,
                       'rates': rates,
                       'notices': notices,
                       'summary_design': summary_design,
                       'summary_endurance': summary_endurance,
                       'summary_cost': summary_cost,
                       'summary_leading': summary_leading,
                       'avarage': average,
                       'num_of_opinions': notices.count(),
                       'num_of_rates': rates.count(),
                       'add_pic': add_pic_form}

                return render(request, 'rate_a_car_app/car-details.html', ctx)
        if 'image' in request.POST:
            img_form = UploadCarPictureForm(request.POST, request.FILES)

            if img_form.is_valid():
                Images.objects.create(carmodel=car,
                                      image=img_form.cleaned_data['image'])

                return redirect(f"/cars/{car.model}/{version}/")
            else:
                car = CarModel.objects.get(model=car, version=version)
                owners = CarOwners.objects.filter(car=car)
                notices = Notice.objects.filter(car=car)
                add_pic_form = UploadCarPictureForm

                if request.user in [own.owner.user for own in owners]:
                    rate_form = RateForm(initial={'carmodel': car,
                                                  'user': request.user})
                    notice_form = NoticeForm(initial={'author': request.user,
                                                      'car': car})
                else:
                    rate_form = None
                    notice_form = None
                rates = Rate.objects.filter(carmodel=car).order_by('-date')[:10]
                if len([rate.design for rate in rates]) > 0:
                    division_by = len([rate.design for rate in rates])
                else:
                    division_by = 1
                summary_design = round(sum([rate.design for rate in rates]) / division_by, 2)
                summary_endurance = round(sum([rate.endurance for rate in rates]) / division_by, 2)
                summary_cost = round(sum([rate.operation_cost for rate in rates]) / division_by, 2)
                summary_leading = round(sum([rate.leading for rate in rates]) / division_by, 2)
                average = (summary_leading + summary_cost + summary_design + summary_endurance) / 4
                car.average_rate = round(average, 2)
                car.save()
                ctx = {'car': car,
                       'rate_form': rate_form,
                       'notice_form': notice_form,
                       'rates': rates,
                       'notices': notices,
                       'summary_design': summary_design,
                       'summary_endurance': summary_endurance,
                       'summary_cost': summary_cost,
                       'summary_leading': summary_leading,
                       'avarage': average,
                       'num_of_opinions': notices.count(),
                       'num_of_rates': rates.count(),
                       'add_pic': add_pic_form,
                       'error': 'error'}

                return render(request, 'rate_a_car_app/car-details.html', ctx)




class AddNoticeView(LoginRequiredMixin, View):

    def post(self, request, car, version):
        form = NoticeForm(request.POST)
        car = CarModel.objects.get(model=car, version=version)
        if form.is_valid():
            Notice.objects.create(author=request.user,
                                  car=car,
                                  content=form.cleaned_data['content'])
            return redirect(f"/cars/{car.model}/{car.version}/")
        else:
            return redirect(f"/cars/{car.model}/{car.version}/")


class UserProfileView(View):
    """Loged user profile

    View allows user to browse user informations, car history and last notices"""

    def get(self, request, user):
        user_obj = User.objects.get(username=user)
        cars = CarOwners.objects.filter(owner=Profile.objects.get(user=user_obj))
        last_notices = Notice.objects.filter(author=user_obj).order_by('-date')
        ctx = {'user': user_obj,
               'cars': cars,
               'notices': last_notices}
        return render(request, 'rate_a_car_app/user-view.html', ctx)


class AddCarHistoryView(View):
    """Add car to user history"""
    def get(self, request, user):
        user = User.objects.get(username=user)
        form = AddCarsHistoryForm(initial={'owner': user.id})
        cars = CarModel.objects.order_by('brand')
        brands = Brand.objects.all()
        ctx = {'user_car_history': CarOwners.objects.filter(owner=Profile.objects.get(user=user)).order_by('use_from'),
               'add_car': form,
               'all_cars': cars,
               'brands': brands,}
        return render(request, 'rate_a_car_app/car-history.html', ctx)

    def post(self, request, user):

        user_obj = User.objects.get(username=user)
        profile = Profile.objects.get(user=user_obj)
        form = AddCarsHistoryForm(request.POST)
        if form.is_valid():
            car = form.cleaned_data['car']
            CarOwners.objects.create(car_id=CarModel.objects.filter(model__in=car, version__in=car),
                                     owner=profile,
                                     use_from=form.cleaned_data['use_from'],
                                     use_to=form.cleaned_data['use_to'])
            return redirect(f"/profile/history/{user}/")
        else:
            user = User.objects.get(username=user)
            form = AddCarsHistoryForm(initial={'owner': user.id})
            ctx = {'user_car_history': CarOwners.objects.filter(owner=user.id),
                   'add_car': form}
            return render(request, 'rate_a_car_app/car-history.html', ctx)


class RemoveFromHistoryView(View):
    """Class remove car from user cars history

    After remove we're redirected to user profile view"""

    def post(self, request, user, car, version):
        user_obj = User.objects.get(username=user)
        car_obj = CarModel.objects.get(model=car, version=version)
        CarOwners.objects.get(owner=user_obj.profile, car=car_obj).delete()
        return redirect(f"/profile/history/{user}/")


class SettingsView(View):
    def get(self, request):
        form = SettingsDataForm(initial={'username': request.user.username,
                                         'first_name': request.user.first_name,
                                         'last_name': request.user.last_name,
                                         'email': request.user.email})
        new_password_form = SettingsChangePasswordForm()
        new_avatar_form = UpdateAvatarForm
        ctx = {'form': form,
               'new_pass': new_password_form,
               'new_avatar': new_avatar_form}
        return render(request, 'rate_a_car_app/settings.html', ctx)

    def post(self, request):
        user = User.objects.get(username=request.user.username)
        if 'data' in request.POST:
            form = SettingsDataForm(request.POST)
            if form.is_valid():
                user.username = form.cleaned_data['username']
                user.first_name = form.cleaned_data['first_name']
                user.last_name = form.cleaned_data['last_name']
                user.email = form.cleaned_data['email']
                user.save()
                return redirect('/settings/')
            else:
                form = SettingsDataForm(initial={'username': request.user.username,
                                                 'first_name': request.user.first_name,
                                                 'last_name': request.user.last_name,
                                                 'email': request.user.email})
                new_password_form = SettingsChangePasswordForm()
                new_avatar_form = UpdateAvatarForm
                ctx = {'form': form,
                       'new_pass': new_password_form,
                       'new_avatar': new_avatar_form,
                       'error': 'Coś poszło nie tak'}
                return render(request, 'rate_a_car_app/settings.html', ctx)

        if 'password' in request.POST:
            form = SettingsChangePasswordForm(request.POST)
            if form.is_valid():
                if request.user.password == form.cleaned_data['password1']:
                    form = SettingsDataForm(initial={'username': request.user.username,
                                                     'first_name': request.user.first_name,
                                                     'last_name': request.user.last_name,
                                                     'email': request.user.email})
                    new_password_form = SettingsChangePasswordForm()
                    ctx = {'form': form,
                           'new_pass': new_password_form,
                           'error_pass': 'Nowe hasło musi się różnić od poprzedniego'}
                    return render(request, 'rate_a_car_app/settings.html', ctx)
                else:
                    request.user.set_password = form.cleaned_data['password1']
                    return redirect('/settings/')
            else:
                form = SettingsDataForm(initial={'username': request.user.username,
                                                 'first_name': request.user.first_name,
                                                 'last_name': request.user.last_name,
                                                 'email': request.user.email})
                new_password_form = SettingsChangePasswordForm()
                new_avatar_form = UpdateAvatarForm
                ctx = {'form': form,
                       'new_pass': new_password_form,
                       'new_avatar': new_avatar_form,
                       'error': 'Coś poszło nie tak'}
                return render(request, 'rate_a_car_app/settings.html', ctx)

        if 'avatar' in request.POST:
            form = UpdateAvatarForm(request.POST)
            if form.is_valid():
                profile= Profile.objects.get(user=request.user)
                profile.avatar = form.cleaned_data['avatar']
                profile.save()
                return redirect('/settings/')
            else:
                form = SettingsDataForm(initial={'username': request.user.username,
                                                 'first_name': request.user.first_name,
                                                 'last_name': request.user.last_name,
                                                 'email': request.user.email})
                new_password_form = SettingsChangePasswordForm()
                new_avatar_form = UpdateAvatarForm
                ctx = {'form': form,
                       'new_pass': new_password_form,
                       'new_avatar': new_avatar_form,
                       'error': 'Coś poszło nie tak'}
                return render(request, 'rate_a_car_app/settings.html', ctx)




class DeleteAccount(LoginRequiredMixin, View):

    def post(self, request):
        u = request.user
        u.delete()
        return redirect('/')

from django.contrib.auth import logout, authenticate, login, get_user_model
from django.contrib.auth.models import User
from django.db.models import Sum
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.core.paginator import Paginator
# Create your views here.
from django.views import View

from .forms import LoginForm, NewBrandForm, NewModelForm, AddCarsHistoryForm, ForgotPassForm, RegisterUserForm, RateForm
from .models import Brand, CarModel, Profile, CarOwners, Rate


def average_rates(rate, rate_query):
    result = sum([rate.rate_query for rate in rate])/len([rate.rate_query for rate in rate])
    if isinstance(result, float):
        return result
    else:
        return 0


class IndexView(View):
    """Display aplications main page
    """
    def get(self, request):
        new_cars = CarModel.objects.order_by('brand')
        paginator = Paginator(new_cars, 10)
        page = request.GET.get('page')
        new_cars_pagination = paginator.get_page(page)
        cnt = {'cars': new_cars_pagination}
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
        return render(request, 'rate_a_car_app/new-password.html', {'form':form})

    def post(self, request):
        """Set password for user type in username field, if password fields isn't the same,
        user is informed about it"""
        form = ForgotPassForm(request.POST)
        if form.is_valid():
            if form.cleaned_data['new_pass1'] != form.cleaned_data['new_pass2']:
                form = ForgotPassForm()
                return render(request, 'rate_a_car_app/new-password.html', {'form': form, 'error':'Hasła muszą być identyczne'})
            else:
                user = User.objects.get(username=form.cleaned_data['user'])
                user.set_password(form.cleaned_data['new_pass1'])
                user.save()
                return redirect('/login/')
        else:
            form = ForgotPassForm()
            return render(request, 'rate_a_car_app/new-password.html', {'form': form, 'error':'Somethings wrong'})

class RegisterView(View):
    """new user register"""
    def get(self, request):
        form_user = RegisterUserForm()
        return render(request, 'rate_a_car_app/register.html', {'form_user':form_user})

    def post(self, request):
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            if form.cleaned_data['password1'] == form.cleaned_data['password2']:
                user = User.objects.create(username=form.cleaned_data['username'],
                                    password=form.cleaned_data['password1'],
                                    first_name=form.cleaned_data['first_name'],
                                    last_name=form.cleaned_data['last_name'],
                                    email=form.cleaned_data['email'])
                Profile.objects.create(user=user)
                return redirect('/')
            else:
                form_user = RegisterUserForm()
                return render(request, 'rate_a_car_app/register.html', {'form_user': form_user, 'error':'Hasła muszą być identyczne'})
        else:
            form_user = RegisterUserForm()
            return render(request, 'rate_a_car_app/register.html', {'form_user': form_user})


class NewBrandView(LoginRequiredMixin, View):
    """View adding new brand to database
    only for loged users"""
    login_url = '/login'
    redirect_field_name = '/create'
    def get(self, request):
        ctx = {
            'add_brand': NewBrandForm(),
        }
        return render(request, 'rate_a_car_app/create-brand.html', ctx)

    def post(self, request):
        add_brand = NewBrandForm(request.POST)
        if add_brand.is_valid():
            Brand.objects.create(brand=add_brand.cleaned_data['brand'])
            return redirect('/')
        else:
            ctx = {
                'add_brand': NewBrandForm(),
            }
            return render(request, 'rate_a_car_app/create-brand.html', ctx)


class NewModelView(LoginRequiredMixin, View):
    """Adding new car model with model name, version and years of production
    only for loged users"""
    login_url = '/login'
    redirect_field_name = 'new-model'
    def get(self, request):
        ctx = {'add_model': NewModelForm()}
        return render(request, 'rate_a_car_app/create-model.html', ctx)

    def post(self, request):
        add_model = NewModelForm(request.POST)
        if add_model.is_valid():
            CarModel.objects.create(brand=add_model.cleaned_data['brand'],
                                    model=add_model.cleaned_data['model'],
                                    version=add_model.cleaned_data['version'],
                                    production_from=add_model.cleaned_data['production_from'],
                                    production_to=add_model.cleaned_data['production_to'])
            return redirect('/')
        else:
            ctx = {'add_model': NewModelForm()}
            return render(request, 'rate_a_car_app/create-brand.html', ctx)


class BrowseCarView(View):
    """Most important view in project

    User can browse a car filtering by brand and simply skip to car details"""
    def get(self, request):
        ctx = {'new_car': CarModel.objects.all().order_by('brand'),
               'brands':Brand.objects.all()}
        return render(request, 'rate_a_car_app/cars.html', ctx)

class BrowseBrandModelsView(View):
    """Based on BrowseCarView

    Car list filtering by brand"""
    def get(self, request, brand_name):
        brand = Brand.objects.get(brand=brand_name)
        ctx = {'cars': CarModel.objects.filter(brand=brand.id).order_by('model'),
               'brands':Brand.objects.all(),
               'brand_name':brand}
        return render(request, 'rate_a_car_app/brand-cars.html', ctx)

class CarDetailsView(View):
    """Car details

    Information about car, rates, notices"""
    def get(self, request, version, car):
        car = CarModel.objects.get(model=car, version=version)
        rate_form = RateForm(initial={'carmodel': car,
                                      'user': request.user})
        rates = Rate.objects.filter(carmodel=car)[:10]
        if len([rate.design for rate in rates]) > 0:
            division_by = len([rate.design for rate in rates])
        else:
            division_by = 1
        ctx = {'car':car,
               'rate_form':rate_form,
               'rates':rates,
               'summary_design': sum([rate.design for rate in rates])/division_by,
               'summary_endurance': sum([rate.endurance for rate in rates])/division_by,
               'summary_cost': sum([rate.operation_cost for rate in rates])/division_by,
               'summary_leading': sum([rate.leading for rate in rates])/division_by}

        return render(request, 'rate_a_car_app/car-details.html', ctx)

    def post(self, request, car, version):
        form = RateForm(request.POST)
        car = CarModel.objects.get(model=car, version=version)
        if form.is_valid():
            Rate.objects.create(design=form.cleaned_data['design'],
                                leading=form.cleaned_data['leading'],
                                operation_cost=form.cleaned_data['operation_cost'],
                                endurance=form.cleaned_data['endurance'],
                                carmodel=car,
                                user=request.user)
            return redirect(f"/cars/{car.model}/{version}/")
        else:
            rate_form = RateForm()
            car = CarModel.objects.get(model=car, version=version)
            ctx = {'car': car,
                   'rate_form': rate_form}

            return render(request, 'rate_a_car_app/car-details.html', ctx)


class UserProfileView(View):
    """Loged user profile

    View allows user to browse user informations, car history and last notices"""
    def get(self, request, user):
        user_obj = User.objects.get(username=user)
        ctx = {'user': user_obj,
               'cars':CarOwners.objects.filter(owner=Profile.objects.get(user=user_obj))}
        return render(request, 'rate_a_car_app/user-view.html', ctx)

class AddCarHistoryView(View):
    """Add car to user history"""
    def get(self, request, user):
        user = User.objects.get(username=user)
        form = AddCarsHistoryForm(initial={'owner': user.id})
        ctx = {'user_car_history': CarOwners.objects.filter(owner=Profile.objects.get(user=user)),
               'add_car': form}
        return render(request, 'rate_a_car_app/car-history.html', ctx)

    def post(self, request, user):

        user_obj = User.objects.get(username=user)
        profile = Profile.objects.get(user=user_obj)
        form = AddCarsHistoryForm(request.POST)
        if form.is_valid():
            car = form.cleaned_data['car']
            CarOwners.objects.create(car_id=car.id,
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
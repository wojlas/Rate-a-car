from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.core.paginator import Paginator
# Create your views here.
from django.views import View

from .forms import LoginForm, NewBrandForm, NewModelForm, AddCarsHistoryForm
from .models import Brand, CarModel, Owner, CarOwners


class IndexView(View):
    def get(self, request):
        new_cars = CarModel.objects.order_by('brand')
        paginator = Paginator(new_cars, 10)
        page = request.GET.get('page')
        new_cars_pagination = paginator.get_page(page)
        cnt = {'cars': new_cars_pagination}
        return render(request, 'rate_a_car_app/index.html', cnt)


class LoginView(View):
    def get(self, request):
        form = LoginForm()
        return render(request, 'rate_a_car_app/login.html', {'form': form})

    def post(self, request):
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
    def get(self, request):
        logout(request)
        return redirect('/')

class NewBrandView(LoginRequiredMixin, View):
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
    def get(self, request):
        ctx = {'new_car': CarModel.objects.all().order_by('brand'),
               'brands':Brand.objects.all()}
        return render(request, 'rate_a_car_app/cars.html', ctx)

class BrowseBrandModelsView(View):
    def get(self, request, brand_name):
        brand = Brand.objects.get(brand=brand_name)
        ctx = {'cars': CarModel.objects.filter(brand=brand.id).order_by('model'),
               'brands':Brand.objects.all(),
               'brand_name':brand}
        return render(request, 'rate_a_car_app/brand-cars.html', ctx)

class CarDetailsView(View):
    def get(self, request, version, car):
        car = CarModel.objects.get(model=car, version=version)
        ctx = {'car':car}
        return render(request, 'rate_a_car_app/car-details.html', ctx)

class UserProfileView(View):
    def get(self, request, user):
        user = User.objects.get(username=user)
        ctx = {'user': user,
               'cars':CarOwners.objects.filter(owner=user.pk)}
        return render(request, 'rate_a_car_app/user-view.html', ctx)

class AddCarHistoryView(View):
    def get(self, request, user):
        user = User.objects.get(username=user)
        form = AddCarsHistoryForm(initial={'owner': user.id})
        ctx = {'user_car_history': CarOwners.objects.filter(owner=user.id),
               'add_car': form}
        return render(request, 'rate_a_car_app/car-history.html', ctx)

    def post(self, request, user):
        user = User.objects.get(username=user)
        owner = CarOwners.objects.get(user=user)
        form = AddCarsHistoryForm(request.POST)
        if form.is_valid():
            car = form.cleaned_data['car']
            CarOwners.objects.create(car_id=car.id,
                                     owner=Owner.ob,
                                     use_from=form.cleaned_data['use_from'],
                                     use_to=form.cleaned_data['use_to'])
            return redirect(f"/profile/history/{user.username}/")
        else:
            user = User.objects.get(username=user)
            form = AddCarsHistoryForm(initial={'owner': user.id})
            ctx = {'user_car_history': CarOwners.objects.filter(owner=user.id),
                   'add_car': form}
            return render(request, 'rate_a_car_app/car-history.html', ctx)
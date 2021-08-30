from django.contrib.auth import logout, authenticate, login
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
# Create your views here.
from django.views import View

from .forms import LoginForm, NewBrandForm, NewModelForm
from .models import Brand, Car, CarModel


class IndexView(View):
    def get(self, request):
        cnt = {'cars': CarModel.objects.order_by('brand')}
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
                                    name=add_model.cleaned_data['name'],
                                    version=add_model.cleaned_data['version'],
                                    production_from=add_model.cleaned_data['production_from'],
                                    production_to=add_model.cleaned_data['production_to'])
            return redirect('/')
        else:
            ctx = {'add_model': NewModelForm()}
            return render(request, 'rate_a_car_app/create-brand.html', ctx)

from django.contrib.auth import logout, authenticate, login
from django.shortcuts import render, redirect
# Create your views here.
from django.views import View

from .forms import LoginForm


class IndexView(View):
    def get(self, request):
        cnt = {}
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

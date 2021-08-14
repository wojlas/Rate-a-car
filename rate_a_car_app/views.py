from django.shortcuts import render

# Create your views here.
from django.views import View


class TestView(View):
    def get(self, request):
        return render(request, 'rate_a_car_app/base.html')
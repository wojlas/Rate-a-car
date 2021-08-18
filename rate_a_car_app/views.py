from django.shortcuts import render

# Create your views here.
from django.views import View
from django.views.generic import CreateView
from rate_a_car_app.models import Car


class IndexView(View):
    def get(self, request):
        return render(request, 'rate_a_car_app/index.html')

class CreateCarView(CreateView):
    model = Car
    fields = 'brand','car_model'
    success_url = ''
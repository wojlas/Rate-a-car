from django.shortcuts import render

# Create your views here.
from django.views import View
from django.views.generic import CreateView
from rate_a_car_app.models import Car
from rate_a_car_app.forms import AddBrandForm, AddCarForm


class IndexView(View):
    def get(self, request):
        cnt = {'cars': Car.objects.all().order_by('brand', 'car_model')}
        return render(request, 'rate_a_car_app/index.html', cnt)

class CreateCarView(View):
    def get(self, request):
        add_car_form = AddCarForm()
        create_brand_form = AddBrandForm
        return render(request, 'rate_a_car_app/create-car.html', {'add_car_form': add_car_form,
                                                                  'create_brand_form': create_brand_form})

    def post(self, request):
        if AddCarForm(request.POST):
            add_car_form = AddCarForm(request.POST)
            if add_car_form.is_valid():
                add_car_form.save()
                return render(request, 'rate_a_car_app/index.html')

        elif AddBrandForm(request.POST):
            create_brand_form = AddBrandForm(request.POST)
            if create_brand_form.is_valid():
                create_brand_form.save()
                return render(request, 'rate_a_car_app/create-car.html')
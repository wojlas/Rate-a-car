from faker import Faker, Factory
from rate_a_car_app.models import Brand, CarModel
from random import randint

faker = Faker()
def create_model_name():
    f = Factory.create("en_us")
    last_name = f.last_name
    return last_name


def create_fake_models():
    brands = Brand.objects.all()
    for brand in brands:
        for mod in range(5, 10):
             production_from = range(1990,2005)
             production_to = production_from + range(5,10)
             CarModel.objects.create(brand=brand,
                                     model=create_model_name(),
                                     version=faker.currency_code(),
                                     production_from=production_from,
                                     production_to=production_to)
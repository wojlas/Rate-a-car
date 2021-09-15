from django.contrib.auth.models import User
from faker import Faker

from rate_a_car_app.models import CarModel, Brand

faker = Faker("pl_PL")

def fake_user():
    d = faker.simple_profile()
    return {'username': d['username'],
            'password': faker.name(),
            'first_name': faker.name(),
            'last_name': faker.name(),
            'email': faker.email()}

def create_fake_user():
    User.objects.create_user(**fake_user())

def create_fake_user_with_second_pass():
    data = fake_user()
    data['password2'] = data['password']
    data['password1'] = data['password']
    return data

def fake_brand():
    return {'brand': faker.name()}

def create_fake_same_pass():
    password = faker.name()
    return {'password1': password,
            'password2': password}

def fake_car_data():
    brand = Brand.objects.first()
    return {'brand': brand.id,
            'model': faker.name(),
            'version': faker.name(),
            'production_from': faker.pyint(max_value=2021),
            'production_to': faker.pyint(max_value=2021)}

def create_car_brand():
    Brand.objects.create(**fake_brand())
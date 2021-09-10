from django.contrib.auth.models import User
from faker import Faker

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

def fake_model():
    return {}
from PIL import Image
from django.contrib.auth.models import User
from faker import Faker
import io

from rate_a_car_app.models import CarModel, Brand, Images

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
    d = faker.simple_profile()
    return {'brand': d['username']}

def create_fake_same_pass():
    password = faker.name()
    return {'password1': password,
            'password2': password}

def fake_car_data():
    return {'brand': Brand.objects.first(),
            'model': faker.name(),
            'version': faker.name(),
            'production_from': faker.pyint(max_value=1980),
            'production_to': faker.pyint(max_value=2021)}

def create_car_brand():
    Brand.objects.create(**fake_brand())

def create_car_models():
    CarModel.objects.create(**fake_car_data())

def generate_photo_file():
    file = io.BytesIO()
    image = Image.new('RGBA', size=(100, 100), color=(155, 0, 0))
    image.save(file, 'png')
    file.name = 'test.png'
    file.seek(0)
    return file

def upload_photo():
    model = CarModel.objects.first()
    Images.objects.create(carmodel=model,
                          image=generate_photo_file())
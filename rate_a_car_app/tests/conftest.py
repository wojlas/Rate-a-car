import pytest
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

from rate_a_car_app.models import User, Brand
from rate_a_car_app.tests.utils import create_fake_user, create_fake_user_with_second_pass, fake_brand, \
    create_car_brand, create_car_models, upload_photo

User = get_user_model()

@pytest.fixture
def loged_user(client):
    test_user = User.objects.create_user("test_login", "test@test.com", "test_haslo")
    client.force_login(test_user)
    return client


@pytest.fixture
def new_user():
    return User.objects.create_user(create_fake_user_with_second_pass)

@pytest.fixture
def set_up():
    Group.objects.create(name='regular')
    for _ in range(10):
        create_fake_user()

@pytest.fixture
def new_car():
    for _ in range(10):
        create_car_brand()

@pytest.fixture
def cars_in_db():
    Brand.objects.create(brand='Ford')
    for _ in range(10):
        create_car_models()

@pytest.fixture
def img():
    Brand.objects.create(brand='Ford')
    for _ in range(10):
        create_car_models()
    for _ in range(10):
        upload_photo()
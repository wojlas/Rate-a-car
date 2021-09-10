import pytest
from django.contrib.auth.models import Group

from rate_a_car_app.models import User, Brand
from rate_a_car_app.tests.utils import create_fake_user, fake_brand


@pytest.fixture
def new_user():
    return User.objects.create_user(username='pytest8',
                                    password='qwerty',
                                    email='abc.cba.pl')

@pytest.fixture
def set_up():
    Group.objects.create(name='regular')
    for _ in range(10):
        create_fake_user()

@pytest.fixture
def new_brand():
    return Brand.objects.create(fake_brand)
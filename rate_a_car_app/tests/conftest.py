import pytest

from rate_a_car_app.models import User


@pytest.fixture
def new_user():
    return User.objects.create_user(username='pytest8',
                                    password='qwerty',
                                    email='abc.cba.pl')

import os
import sys

import pytest

from rate_a_car_app.models import User

sys.path.append(os.path.dirname(__file__))

@pytest.fixture
def new_user():
    return User.objects.create_user(username='Adam',
                               password='qwerty')

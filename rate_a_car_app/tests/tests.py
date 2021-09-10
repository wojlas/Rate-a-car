import pytest
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User

from rate_a_car_app.models import Brand
from rate_a_car_app.tests.utils import create_fake_user_with_second_pass, create_fake_user, fake_user, fake_brand



@pytest.mark.django_db
def test_register_view(client, set_up):
    count_user = User.objects.count()
    new_user = create_fake_user_with_second_pass()
    response = client.post('/register/', new_user)
    assert response.status_code == 302
    assert User.objects.count() == count_user + 1


@pytest.mark.django_db
def test_index_view(client):
    response = client.get('/')

    assert response.status_code == 200


@pytest.mark.django_db
def test_login_view(client, set_up):
    loged_user = User.objects.first()
    response = client.post('/login/', {'login': loged_user.username,
                                       'password':loged_user.password})
    assert response.status_code == 200


@pytest.mark.django_db
def test_add_brand(client):
    brands_before = Brand.objects.count()
    new_brand = fake_brand()
    response = client.post('/create-brand/', {**new_brand})
    assert response.status_code == 302
    assert Brand.objects.count() == brands_before + 1


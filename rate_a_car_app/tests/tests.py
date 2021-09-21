import pytest
from django.contrib.auth.models import User

from rate_a_car_app.models import Brand, Profile, CarModel, Images
from rate_a_car_app.tests.utils import create_fake_user_with_second_pass, fake_brand, create_fake_same_pass, \
    fake_car_data, create_car_models


@pytest.mark.django_db
def test_register_view(client, set_up):
    count_user = User.objects.count()
    new_user = create_fake_user_with_second_pass()
    response = client.post('/register/', new_user)
    assert response.status_code == 302
    assert User.objects.count() == count_user + 1
    assert User.objects.filter(username=new_user['username'])
    assert Profile.objects.get(user__username=new_user['username'])


@pytest.mark.django_db
def test_index_view(client, img):
    response = client.get('/')
    assert response.status_code == 200


@pytest.mark.django_db
def test_login_view(client, set_up):
    new_user = create_fake_user_with_second_pass()
    register_response = client.post('/register/', new_user)
    response = client.post('/login/', {'login': new_user['username'],
                                       'password': new_user['password']})
    assert response.status_code == 302


@pytest.mark.django_db
def test_logout(client, set_up):
    new_user = create_fake_user_with_second_pass()
    register_response = client.post('/register/', new_user)
    response = client.post('/login/', {'login': new_user['username'],
                                       'password': new_user['password']})
    logout_response = client.get('/logout/')

    assert logout_response.status_code == 302


@pytest.mark.django_db
def test_forgot_pass(client, set_up):
    new_user = create_fake_user_with_second_pass()
    new_password = create_fake_same_pass()
    register_response = client.post('/register/', new_user)
    reset_response = client.post('/reset/', {'user': new_user['username'],
                                             'new_pass1': new_password['password1'],
                                             'new_pass2': new_password['password2']})

    assert reset_response.status_code == 302


@pytest.mark.django_db
def test_add_brand(client, new_car):
    brands_before = Brand.objects.count()
    new_brand = fake_brand()
    response = client.post('/create-brand/', {**new_brand})
    assert response.status_code == 302
    assert Brand.objects.count() == brands_before + 1
    assert Brand.objects.filter(brand=new_brand['brand'])


@pytest.mark.django_db
def test_create_model(client, cars_in_db):
    models_before = CarModel.objects.count()
    new_model = fake_car_data()
    response = client.post('/create-model/', {**new_model})
    assert response.status_code == 302


@pytest.mark.django_db
def test_browse_car(client):
    response = client.get('/cars/')

    assert response.status_code == 200

@pytest.mark.django_db
def test_browse_car_model(client):
    new_brand = fake_brand()
    new_brand_response = client.post('/create-brand/', {**new_brand})
    response = client.get(f"/cars/{new_brand['brand']}/")

    assert response.status_code == 200

@pytest.mark.django_db
def test_car_details(client, cars_in_db):
    car = CarModel.objects.first()
    response = client.get(f'/cars/{car.model}/{car.version}/')

    assert response.status_code == 200
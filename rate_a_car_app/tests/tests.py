import pytest
from django.contrib.auth import authenticate
from django.contrib.auth.models import User

from rate_a_car_app.models import Brand, Profile, CarModel, Notice
from rate_a_car_app.tests.utils import create_fake_user_with_second_pass, fake_brand, create_fake_same_pass, \
    fake_car_data


@pytest.mark.django_db
def test_register_view(client, set_up):
    count_user = User.objects.count()
    new_user = create_fake_user_with_second_pass()
    response = client.post('/register/', new_user)
    assert response.status_code == 302
    assert User.objects.count() == count_user + 1
    assert User.objects.filter(username=new_user['username'])
    assert Profile.objects.get(user__username=new_user['username'])


@pytest.mark.skip('Waiting for image fixture')
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
    user = authenticate(username=new_user['username'], password=new_user['password'])
    assert response.status_code == 302
    assert user != None


@pytest.mark.django_db
def test_logout(loged_user, set_up):
    logout_response = loged_user.get('/logout/')

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
    new_model = fake_car_data()
    response = client.post('/create-model/', {**new_model})
    assert response.status_code == 302


@pytest.mark.django_db
def test_browse_car(client):
    response = client.get('/cars/')

    assert response.status_code == 200


@pytest.mark.django_db
def test_browse_car_model(client, new_car):
    brand = Brand.objects.first()
    response = client.get(f'/cars/{brand.brand}/')

    assert response.status_code == 200


@pytest.mark.django_db
def test_car_details(client, cars_in_db):
    car = CarModel.objects.first()
    response = client.get(f'/cars/{car.model}/{car.version}/')

    assert response.status_code == 200


@pytest.mark.django_db
def test_contact(client):
    response = client.get('/contact/')
    assert response.status_code == 200


@pytest.mark.django_db
def test_regulations(client):
    response = client.get('/regulations/')
    assert response.status_code == 200


@pytest.mark.django_db
def test_faq(client):
    response = client.get('/faq/')
    assert response.status_code == 200


@pytest.mark.django_db
def test_delete_acc(loged_user, set_up):
    users_before = User.objects.count()
    response = loged_user.post('/delete-account/')

    assert response.status_code == 302
    assert User.objects.count() == users_before - 1

@pytest.mark.django_db
def test_add_notice(loged_user, cars_in_db):
    notice_before = Notice.objects.count()
    car = CarModel.objects.first()
    response = loged_user.post(f'/cars/{car.model}/{car.version}/notice/', {'author': loged_user,
                                                                            'car':car,
                                                                            'content': 'test notice from pytest'})

    assert response.status_code == 302
    assert Notice.objects.count() == notice_before + 1

@pytest.mark.django_db
def test_user_profile(client, set_up):
    new_user = create_fake_user_with_second_pass()
    register_response = client.post('/register/', new_user)
    login_response = client.post('/login/', {'login': new_user['username'],
                                       'password': new_user['password']})
    user = authenticate(username=new_user['username'], password=new_user['password'])
    response = client.get(f"/profile/user/{new_user['username']}/")

    assert response.status_code == 200
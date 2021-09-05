import pytest
from django.contrib.auth.models import User


@pytest.mark.django_db
def test_register_view(client, new_user):
    count_user = User.objects.all().count()
    response = client.get('/register/', {'username': 'pytest8',
                                         'password': 'qwerty', })

    assert response.status_code == 200
    assert response.user == 'pytest8'
    assert User.objects.all().count() == count_user + 1


@pytest.mark.django_db
def test_index_view(client):
    response = client.get('/')

    assert response.status_code == 200


@pytest.mark.django_db
def test_login_view(client):
    response = client.get('/login/', {'username': 'pytest8',
                                      'password': 'qwerty'})
    assert response.status_code == 200

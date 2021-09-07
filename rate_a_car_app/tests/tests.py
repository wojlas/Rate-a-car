import pytest
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User


@pytest.mark.skip(reason='nie działa')
@pytest.mark.django_db
def test_register_view(client, new_user):
    count_user = User.objects.all().count()
    response = client.post('/register/', new_user)
    assert User.objects.get(username='pytest8') == new_user
    assert response.status_code == 200
    assert User.objects.all().count() == count_user + 1


@pytest.mark.django_db
def test_index_view(client):
    response = client.get('/')

    assert response.status_code == 200


@pytest.mark.django_db
def test_login_view(client):
    response = client.post('/login/', {'login':'pytest8',
                                       'password':'qwerty'})
    assert response.status_code == 200


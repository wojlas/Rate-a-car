from django.contrib.auth.models import User
from django.test import TestCase
import pytest

# @pytest.mark.django_db
# def test_register_view(client, new_user):
#     response = client.post('/register/', {'username':'Adam',
#                                           'password':'qwerty'})
#
#     assert response.status_code == 302
#     assert User.objects.filter(username='Adam', password='qwerty')

@pytest.mark.django_db
def test_index_view(client):
    response = client.get('/')

    assert response.status_code == 200
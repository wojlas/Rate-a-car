from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _

class RateACarAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'rate_a_car_app'


class UsersConfig(AppConfig):
    name = 'users'
    def ready(self):
        import users.signals

from django.contrib import admin

# Register your models here.
from rate_a_car_app.models import Profile, Brand

admin.site.register(Profile)
admin.site.register(Brand)
from django.db import models
from django.contrib.auth.models import User
RATE_CHOICE = {
    (1, "*"),
    (2, "**"),
    (3, "****"),
    (4, "****"),
    (5, "******"),
    (6, "*******"),
    (7, "********"),
    (8, "*********"),
    (9, "**********"),
    (10, "***********"),
}

class Owner(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    car_history = models.ForeignKey('Car', on_delete=models.CASCADE)
    rates = models.ForeignKey('Rate', on_delete=models.CASCADE)

class Brand(models.Model):
    brand = models.CharField(unique=True, max_length=32)

    def __str__(self):
        return f'{self.brand}'

class CarModel(models.Model):
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    name = models.CharField(max_length=32)
    version = models.CharField(max_length=32)
    production_from = models.IntegerField(null=False)
    production_to = models.IntegerField(null=False)

class Car(models.Model):
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    model = models.ForeignKey(CarModel, on_delete=models.CASCADE)
    rate = models.ForeignKey('Rate', on_delete=models.CASCADE)
    opinions = models.ForeignKey('Notice', on_delete=models.CASCADE)
    owners = models.ForeignKey(Owner, on_delete=models.CASCADE)

class Rate(models.Model):
    endurance = models.IntegerField(choices=RATE_CHOICE)
    operation_cost = models.IntegerField(choices=RATE_CHOICE)
    leading = models.IntegerField(choices=RATE_CHOICE)
    design = models.IntegerField(choices=RATE_CHOICE)

class Notice(models.Model):
    author = models.OneToOneField(User, on_delete=models.CASCADE)
    content = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
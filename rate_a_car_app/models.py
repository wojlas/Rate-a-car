from django.contrib.auth.models import User
from django.db import models

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
    car_history = models.ForeignKey('CarModel', on_delete=models.CASCADE)
    rates = models.ForeignKey('Rate', on_delete=models.CASCADE)


class Brand(models.Model):
    brand = models.CharField(unique=True, max_length=32, verbose_name='Marka')

    class Meta:
        ordering = ['brand']

    def __str__(self):
        return f'{self.brand}'


class CarModel(models.Model):
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, verbose_name='Marka')
    model = models.CharField(max_length=32, verbose_name='Model')
    version = models.CharField(max_length=32, verbose_name='Wersja')
    production_from = models.IntegerField(null=False, verbose_name='Produkcja od')
    production_to = models.CharField(null=True, verbose_name='Produkcja do', default=' - ', max_length=4)
    rate = models.ForeignKey('Rate', on_delete=models.CASCADE, null=True)
    opinions = models.ForeignKey('Notice', on_delete=models.CASCADE, null=True)
    owners = models.ForeignKey(Owner, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f'{self.brand} {self.model}({self.version})'


class Rate(models.Model):
    endurance = models.IntegerField(choices=RATE_CHOICE, verbose_name='Wytrzymałość')
    operation_cost = models.IntegerField(choices=RATE_CHOICE, verbose_name='Koszty utrzymania')
    leading = models.IntegerField(choices=RATE_CHOICE, verbose_name='Prowadzenie')
    design = models.IntegerField(choices=RATE_CHOICE, verbose_name='Wygląd')


class Notice(models.Model):
    author = models.OneToOneField(User, on_delete=models.CASCADE)
    content = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

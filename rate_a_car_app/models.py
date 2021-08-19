from django.db import models

CHOICES = {
    (1, 1),
    (2, 2),
    (3, 3),
    (4, 4),
    (5, 5),
    (6, 6),
    (7, 7),
    (8, 8),
    (9, 9),
    (10, 10),
}


class Rate(models.Model):
    endurance = models.IntegerField(choices=CHOICES, verbose_name='Wytrzymałość')
    leading = models.IntegerField(choices=CHOICES, verbose_name='Prowadzenie')
    operating_cost = models.IntegerField(choices=CHOICES, verbose_name='Koszty eksploatacji')
    design = models.IntegerField(choices=CHOICES, verbose_name='Wygląd')


class Brand(models.Model):
    name = models.CharField(max_length=32, verbose_name='Marka', unique=True)

    def __str__(self):
        return f"{self.name}"


class Car(models.Model):
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, verbose_name='Marka', null=True)
    car_model = models.CharField(max_length=32, verbose_name='Model')
    versions = models.CharField(max_length=32, verbose_name='Wersja')
    year_of_production = models.CharField(max_length=12, verbose_name='Lata produkcji', null=True)
    rate = models.ForeignKey(Rate, on_delete=models.CASCADE, verbose_name='Ocena', null=True)

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


class YearsOfProduction(models.Model):
    year_of_production = models.ValueRange()


class Rate(models.Model):
    endurance = models.IntegerField(choices=CHOICES, verbose_name='Wytrzymałość')
    leading = models.IntegerField(choices=CHOICES, verbose_name='Prowadzenie')
    operating_cost = models.IntegerField(choices=CHOICES, verbose_name='Koszty eksploatacji')
    design = models.IntegerField(choices=CHOICES, verbose_name='Wygląd')


class Brand(models.Model):
    name = models.CharField(max_length=32, verbose_name='Marka')

    def __str__(self):
        return f"{self.name}"


class CarModels(models.Model):
    model_name = models.CharField(max_length=32, verbose_name='Model')
    versions = models.ForeignKey(YearsOfProduction, on_delete=models.CASCADE, verbose_name='Wersja', null=True)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, null=True)


class Car(models.Model):
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, verbose_name='Marka', null=True)
    car_model = models.ForeignKey(CarModels, on_delete=models.CASCADE, verbose_name='Model', null=True)
    rate = models.ForeignKey(Rate, on_delete=models.CASCADE, verbose_name='Ocena', null=True)

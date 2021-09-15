
from django.contrib.auth.models import User
from django.db import models

RATE_CHOICE = [
    (1, "(1)*"),
    (2, "(2)**"),
    (3, "(3)***"),
    (4, "(4)****"),
    (5, "(5)******"),
    (6, "(6)*******"),
    (7, "(7)********"),
    (8, "(8)*********"),
    (9, "(9)**********"),
    (10, "(10)***********"),
]


class Profile(models.Model):
    """Model extend User by one-to-one field"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='static/avatars', default='default.png')
    car_history = models.ManyToManyField('CarModel', through='CarOwners')

    def set_avatar(self):
        self.has_picture = True

    def __str__(self):
        return f"{self.user.username}"



class Brand(models.Model):
    """Car brands model"""
    brand = models.CharField(unique=True, max_length=32, verbose_name='Marka')

    class Meta:
        """Alphabetical order on list all brands"""
        ordering = ['brand']

    def __str__(self):
        return f'{self.brand}'


class CarModel(models.Model):
    """Car models model"""
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, verbose_name='Marka')
    model = models.CharField(max_length=32, verbose_name='Model')
    version = models.CharField(max_length=32, verbose_name='Wersja', null=True)
    production_from = models.IntegerField(null=False, verbose_name='Produkcja od')
    production_to = models.CharField(null=True, verbose_name='Produkcja do', default=' - ', max_length=4)
    opinions = models.ForeignKey('Notice', on_delete=models.CASCADE, null=True)
    owners = models.ManyToManyField(Profile, through='CarOwners')
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.brand} {self.model}({self.version})'


class Rate(models.Model):
    """Models with cars rates"""
    endurance = models.IntegerField(choices=RATE_CHOICE, verbose_name='Wytrzymałość', null=True)
    operation_cost = models.IntegerField(choices=RATE_CHOICE, verbose_name='Koszty utrzymania', null=True)
    leading = models.IntegerField(choices=RATE_CHOICE, verbose_name='Prowadzenie', null=True)
    design = models.IntegerField(choices=RATE_CHOICE, verbose_name='Wygląd', null=True)
    carmodel = models.ForeignKey(CarModel, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    date = models.DateTimeField(auto_now_add=True)




class Notice(models.Model):
    """Model with cars notices"""
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(verbose_name='')
    date = models.DateTimeField(auto_now_add=True)
    car = models.ForeignKey(CarModel, on_delete=models.CASCADE, null=True)

class CarOwners(models.Model):
    """Many to many table between models CarModel and Profile"""
    car = models.ForeignKey(CarModel, on_delete=models.CASCADE, verbose_name='Samochód')
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE)
    use_from = models.IntegerField(null=False, verbose_name='Od')
    use_to = models.CharField(default='-', max_length=4, verbose_name='Do')
    notice = models.ForeignKey(Notice, on_delete=models.CASCADE, null=True)

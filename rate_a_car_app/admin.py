from django.contrib import admin


from rate_a_car_app.models import Profile, Brand, CarModel

admin.site.register(Profile)
admin.site.register(Brand)

@admin.register(CarModel)
class CarModelAdmin(admin.ModelAdmin):
    list_display = ['brand', 'model', 'version', 'production_from', 'production_to']
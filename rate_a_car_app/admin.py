from django.contrib import admin


from rate_a_car_app.models import Profile, Brand, CarModel, Rate, CarOwners, Notice

admin.site.register(Brand)

@admin.register(CarModel)
class CarModelAdmin(admin.ModelAdmin):
    list_display = ['brand', 'model', 'version', 'production_from', 'production_to', 'average_rate']

def default_avatar(model_admin, request, query_set):
    query_set.update(avatar='avatars/default.png')

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'avatar']
    actions = [default_avatar]

@admin.register(Rate)
class RateAdmin(admin.ModelAdmin):
    list_display = ['user', 'carmodel', 'endurance', 'operation_cost', 'leading', 'design', 'date']

@admin.register(CarOwners)
class CarOwnersAdmin(admin.ModelAdmin):
    list_display = ['car', 'owner', 'use_from', 'use_to']

@admin.register(Notice)
class NoticeAdmin(admin.ModelAdmin):
    list_display = ['author', 'car', 'date', 'content']
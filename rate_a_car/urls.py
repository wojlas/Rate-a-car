"""rate_a_car URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from rate_a_car_app.views import IndexView, LoginView, LogoutView, NewBrandView, NewModelView, BrowseCarView,\
    UserProfileView, CarDetailsView, BrowseBrandModelsView, AddCarHistoryView, ForgotPassView, RegisterView,\
    RemoveFromHistoryView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', IndexView.as_view()),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('login/', LoginView.as_view(), name='login'),
    path('reset/', ForgotPassView.as_view(), name='new-password'),
    path('register/', RegisterView.as_view(), name='register'),
    path('create-brand/', NewBrandView.as_view(), name='create-brand'),
    path('create-model/', NewModelView.as_view(), name='create-model'),
    path('cars/', BrowseCarView.as_view(), name='cars'),
    path('cars/<str:brand_name>/', BrowseBrandModelsView.as_view(), name='car-brand'),
    path('cars/<str:car>/<str:version>/', CarDetailsView.as_view(), name='car-details'),
    path('profile/user/<str:user>/', UserProfileView.as_view(), name='user-profile'),
    path('profile/history/<str:user>/', AddCarHistoryView.as_view(), name='car-history'),
    path('profile/history/<str:user>/<str:car>/<str:version>/remove', RemoveFromHistoryView.as_view(), name='remove-car')
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

from django.urls import path
from . import views

urlpatterns = [
    path('', views.profile, name="profile-page"),
    path('<name>/', views.seller_profile, name="seller-profile"),
]


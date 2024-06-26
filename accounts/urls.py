from django.urls import path, register_converter
from .views import *
from utils import HashIdConverter

register_converter(HashIdConverter, "hashid")

urlpatterns = [
    path('signup/', signupView, name='signup'),
    path('login/', loginView, name='login'),
    path('logout/', logoutUser, name='logout'),
    path('users/', users, name='users'),
    path('users/<hashid:pk>/', user_details, name='user_details'),
]

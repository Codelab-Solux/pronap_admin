from django.urls import path, register_converter
from .views import *
from utils import HashIdConverter

register_converter(HashIdConverter, "hashid")

urlpatterns = [
    path('signup/', signupView, name='signup'),
    path('login/', loginView, name='login'),
    path('logout/', logoutUser, name='logout'),
    # ----------------------------------------------------------------------------
    path('staff/', staff, name='staff'),
    path('staff/grid/', staff_grid, name='staff_grid'),
    path('staff/list/', staff_list, name='staff_list'),
    path('staff/create/', create_staff, name='create_staff'),
    path('staff/<hashid:pk>/', staff_details, name='staff_details'),
    path('staff/<hashid:pk>/edit/', edit_staff, name='edit_staff'),
    path('staff/<hashid:pk>/profile/edit/',
         edit_staff_profile, name='edit_staff_profile'),
]

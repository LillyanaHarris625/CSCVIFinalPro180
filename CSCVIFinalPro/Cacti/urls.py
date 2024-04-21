from django.contrib import admin
from django.urls import path
from .views import home,register,login_user,logout_user
from . import views
from django.urls import path
from .views import (
    cactus_list,
    cactus_detail,
    cactus_create,
    cactus_update,
    cactus_delete,
    payment_view,
    process_payment,
)


urlpatterns = [
    path('',home,name="home"),
    path('register/',register,name="register"),
    path('login_user',login_user,name="login_user"),
    path('logout_user',logout_user,name="logout_user"),
    path('create_profile/', views.create_profile, name='create_profile'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('profile_detail/', views.profile_detail, name='profile_detail'),
    path('cactus/', cactus_list, name='cactus_list'),  # URL for listing all cacti
    path('cactus/create/', cactus_create, name='cactus_create'),  # URL for creating a new cactus
    path('cactus/<int:pk>/', cactus_detail, name='cactus_detail'),  # URL for viewing details of a cactus
    path('cactus/<int:pk>/update/', cactus_update, name='cactus_update'),  # URL for updating a cactus
    path('cactus/<int:pk>/delete/', cactus_delete, name='cactus_delete'),  # URL for deleting a cactus
    path('payment/', payment_view, name='payment'),
    path('process_payment/', process_payment, name='process_payment'),

]
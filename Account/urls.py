from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('',views.Login, name = 'Login'),
    path('Register',views.Register, name = 'Register'),
    path('Logout',views.Logout, name = 'Logout'),
    path('User/Dashboard',views.Dashboard, name = 'Dashboard'),
]
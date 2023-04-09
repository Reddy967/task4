from django.contrib import admin
from django.urls import path
from .views import *


urlpatterns = [
    path('', login_view),
    path('register/', register_view),
    path('otp/<uid>/', otp),
    path('dashboard', dashboard_view)
]
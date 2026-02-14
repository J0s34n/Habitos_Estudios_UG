from django.urls import path
from .views import register
from .views import login_view

urlpatterns = [
    path('register/', register),
    path('login/', login_view),
]  
from django.urls import path
from .views import hanghoa_get_all

urlpatterns = [
    path('hanghoa/', hanghoa_get_all),
]
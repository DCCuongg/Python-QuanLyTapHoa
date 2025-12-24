from django.urls import path
from .views import *

urlpatterns = [
    path('hanghoa/', hanghoa_get_all),
    path('hanghoa/<int:ma_hang>/', hanghoa_get_by_id),
    path('hanghoa/create/', hanghoa_create),
    path('hanghoa/<int:ma_hang>/update/', hanghoa_update),
    path('hanghoa/<int:ma_hang>/delete/', hanghoa_delete),
    path('hanghoa/<int:ma_hang>/adjust-stock/', hanghoa_adjust_stock),
]
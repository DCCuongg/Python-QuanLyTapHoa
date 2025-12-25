# urls.py trong app QuanLyHoaDon
from django.urls import path
from QuanLyHoaDon.views import hoa_don_create, hoa_don_get_all

urlpatterns = [
    path('hoadon/create/', hoa_don_create, name='hoa_don_create'),
    path('hoadon/', hoa_don_get_all, name='hoa_don_get_all'),  # thêm API GET tất cả hóa đơn
]

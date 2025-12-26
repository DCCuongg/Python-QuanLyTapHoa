"""
URL configuration for QuanLyNhanSu app.
"""
from django.urls import path
from .views import *

urlpatterns = [
    # Chức vụ APIs
    path('chucvu/', chucvu_get_all),                          # GET: Lấy tất cả chức vụ
    path('chucvu/<int:ma_chuc_vu>/', chucvu_get_by_id),       # GET: Lấy chức vụ theo ID
    path('chucvu/create/', chucvu_create),                    # POST: Tạo chức vụ mới
    path('chucvu/<int:ma_chuc_vu>/update/', chucvu_update),   # PUT: Cập nhật chức vụ
    path('chucvu/<int:ma_chuc_vu>/delete/', chucvu_delete),   # DELETE: Xóa chức vụ
    
    # Nhân viên APIs
    path('nhanvien/', nhanvien_get_all),                      # GET: Lấy tất cả nhân viên
    path('nhanvien/<int:ma_nv>/', nhanvien_get_by_id),        # GET: Lấy nhân viên theo ID
    path('nhanvien/create/', nhanvien_create),                # POST: Tạo nhân viên mới
    path('nhanvien/<int:ma_nv>/update/', nhanvien_update),    # PUT: Cập nhật nhân viên
    path('nhanvien/<int:ma_nv>/delete/', nhanvien_delete),    # DELETE: Xóa nhân viên
    
    # Tìm kiếm và lọc
    path('nhanvien/search/', nhanvien_search),                # GET: Tìm kiếm nhân viên theo tên
    path('nhanvien/filter/', nhanvien_filter_by_chucvu),      # GET: Lọc nhân viên theo chức vụ
]
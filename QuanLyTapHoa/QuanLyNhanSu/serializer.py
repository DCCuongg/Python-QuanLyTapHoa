from rest_framework import serializers
from QuanLyNhanSu.models.chuc_vu import ChucVu
from QuanLyNhanSu.models.nhan_vien import NhanVien

# Serializer cho ChucVu
class ChucVuSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChucVu
        fields = ['ma_chuc_vu', 'ten_chuc_vu', 'phu_cap', 'he_so_luong', 'ghi_chu']


# Serializer cho NhanVien
class NhanVienSerializer(serializers.ModelSerializer):
    # show tên chức vụ kèm mã chức vụ
    ten_chuc_vu = serializers.CharField(source='ma_chuc_vu.ten_chuc_vu', read_only=True)

    class Meta:
        model = NhanVien
        fields = ['ma_nv', 'ho_ten', 'ma_chuc_vu', 'ten_chuc_vu', 'sdt', 'dia_chi']

"""
Module định nghĩa Model và Repository cho bảng NHAN_VIEN.

- NhanVien: thông tin nhân viên
- NhanVienRepository: thao tác dữ liệu nhân viên (CRUD)
"""

from django.db import models
from typing import Optional
from django.db.models import QuerySet


# =========================
# Model cho bảng NHAN_VIEN
# =========================
class NhanVien(models.Model):
    """
    Model đại diện cho bảng NHAN_VIEN.

    Attributes:
        ma_nv (int): Mã nhân viên
        ho_ten (str): Họ tên nhân viên
        ma_chuc_vu (ChucVu): Chức vụ của nhân viên
        sdt (str): Số điện thoại
        dia_chi (str): Địa chỉ
    """

    ma_nv = models.AutoField(
        primary_key=True,
        db_column='MaNV'
    )

    ho_ten = models.CharField(
        max_length=100,
        null=False,
        db_column='HoTen'
    )

    ma_chuc_vu = models.ForeignKey(
        'ChucVu',
        on_delete=models.PROTECT,
        db_column='MaChucVu',
        related_name='nhan_viens'
    )

    sdt = models.CharField(
        max_length=15,
        null=True,
        blank=True,
        db_column='SDT'
    )

    dia_chi = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        db_column='DiaChi'
    )

    class Meta:
        db_table = 'NHAN_VIEN'
        managed = False

    def __str__(self):
        return f"{self.ho_ten} (#{self.ma_nv})"


# =========================
# Repository cho NHAN_VIEN
# =========================
class NhanVienRepository:
    """
    Repository xử lý truy vấn và thao tác dữ liệu Nhân viên.
    """

    @staticmethod
    def get_all() -> QuerySet[NhanVien]:
        """
        Lấy danh sách tất cả nhân viên (kèm chức vụ).
        """
        return NhanVien.objects.select_related('ma_chuc_vu')

    @staticmethod
    def get_by_id(ma_nv: int) -> Optional[NhanVien]:
        """
        Lấy nhân viên theo mã.
        """
        return (
            NhanVien.objects
            .select_related('ma_chuc_vu')
            .filter(pk=ma_nv)
            .first()
        )

    @staticmethod
    def create(
        ho_ten: str,
        ma_chuc_vu: int,
        sdt: str = None,
        dia_chi: str = None
    ) -> NhanVien:
        """
        Tạo mới nhân viên.
        """
        obj = NhanVien(
            ho_ten=ho_ten,
            ma_chuc_vu_id=ma_chuc_vu,
            sdt=sdt,
            dia_chi=dia_chi
        )
        obj.save()
        return obj

    @staticmethod
    def update(ma_nv: int, **kwargs) -> Optional[NhanVien]:
        """
        Cập nhật thông tin nhân viên.
        """
        obj = NhanVienRepository.get_by_id(ma_nv)
        if not obj:
            return None

        if 'ho_ten' in kwargs:
            obj.ho_ten = kwargs['ho_ten']

        if 'ma_chuc_vu' in kwargs:
            obj.ma_chuc_vu_id = kwargs['ma_chuc_vu']

        if 'sdt' in kwargs:
            obj.sdt = kwargs['sdt']

        if 'dia_chi' in kwargs:
            obj.dia_chi = kwargs['dia_chi']

        obj.save()
        return obj

    @staticmethod
    def delete(ma_nv: int) -> bool:
        """
        Xóa nhân viên theo mã.
        """
        obj = NhanVienRepository.get_by_id(ma_nv)
        if not obj:
            return False
        obj.delete()
        return True

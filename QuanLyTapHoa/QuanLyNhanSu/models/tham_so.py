"""
Module quản lý tham số lương trong hệ thống.

Bao gồm:
- Model ThamSoLuong: ánh xạ bảng THAM_SO_LUONG trong CSDL
- ThamSoLuongRepository: tầng truy cập dữ liệu (CRUD + nghiệp vụ đọc lương cơ bản)

Mục đích:
- Lưu trữ các tham số ảnh hưởng đến tính lương (ví dụ: Lương cơ bản)
- Cho phép thay đổi theo thời gian thông qua ngày hiệu lực
"""

from django.db import models
from typing import Optional
from django.db.models import QuerySet


class ThamSoLuong(models.Model):
    """
    Model biểu diễn bảng THAM_SO_LUONG.

    Dùng để lưu các tham số cấu hình cho lương:
    - Có thể là giá trị số (gia_tri_so)
    - Hoặc giá trị chữ (gia_tri_chu)
    - Áp dụng theo ngày hiệu lực
    """

    ma_tham_so = models.AutoField(
        primary_key=True,
        db_column='MaThamSo'
    )

    ten_tham_so = models.CharField(
        max_length=100,
        db_column='TenThamSo'
    )

    gia_tri_so = models.DecimalField(
        max_digits=18,
        decimal_places=2,
        null=True,
        blank=True,
        db_column='GiaTriSo'
    )

    gia_tri_chu = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        db_column='GiaTriChu'
    )

    ngay_hieu_luc = models.DateField(
        db_column='NgayHieuLuc'
    )

    ghi_chu = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        db_column='GhiChu'
    )

    class Meta:
        db_table = 'THAM_SO_LUONG'
        managed = False  # DB có sẵn

    def __str__(self):
        return self.ten_tham_so


class ThamSoLuongRepository:
    """
    Repository cho ThamSoLuong.

    Chịu trách nhiệm:
    - Truy vấn dữ liệu tham số lương
    - Tách biệt logic DB khỏi Service / View
    """

    @staticmethod
    def get_luong_co_ban_hien_tai() -> Optional[ThamSoLuong]:
        """
        Lấy tham số lương cơ bản đang hiệu lực mới nhất.

        Trả về:
        - ThamSoLuong hoặc None nếu chưa có
        """
        return (
            ThamSoLuong.objects
            .filter(ten_tham_so='LuongCoBan')
            .order_by('-ngay_hieu_luc')
            .first()
        )

    @staticmethod
    def get_all() -> QuerySet[ThamSoLuong]:
        """
        Lấy danh sách tất cả tham số lương.
        """
        return ThamSoLuong.objects.all()

    @staticmethod
    def get_by_id(ma_tham_so: int) -> Optional[ThamSoLuong]:
        """
        Lấy tham số lương theo ID.
        """
        try:
            return ThamSoLuong.objects.get(pk=ma_tham_so)
        except ThamSoLuong.DoesNotExist:
            return None

    @staticmethod
    def get_by_ten(ten_tham_so: str) -> Optional[ThamSoLuong]:
        """
        Lấy tham số lương theo tên (bản ghi mới nhất theo ngày hiệu lực).
        """
        return (
            ThamSoLuong.objects
            .filter(ten_tham_so=ten_tham_so)
            .order_by('-ngay_hieu_luc')
            .first()
        )

    @staticmethod
    def create(
        ten_tham_so: str,
        gia_tri_so: float = None,
        gia_tri_chu: str = None,
        ngay_hieu_luc=None,
        ghi_chu: str = None
    ) -> ThamSoLuong:
        """
        Tạo mới một tham số lương.
        """
        obj = ThamSoLuong(
            ten_tham_so=ten_tham_so,
            gia_tri_so=gia_tri_so,
            gia_tri_chu=gia_tri_chu,
            ngay_hieu_luc=ngay_hieu_luc,
            ghi_chu=ghi_chu
        )
        obj.save()
        return obj

    @staticmethod
    def update(ma_tham_so: int, **kwargs) -> Optional[ThamSoLuong]:
        """
        Cập nhật tham số lương theo ID.
        """
        obj = ThamSoLuongRepository.get_by_id(ma_tham_so)
        if not obj:
            return None

        for key, value in kwargs.items():
            if hasattr(obj, key):
                setattr(obj, key, value)

        obj.save()
        return obj

    @staticmethod
    def delete(ma_tham_so: int) -> bool:
        """
        Xóa tham số lương theo ID.
        """
        obj = ThamSoLuongRepository.get_by_id(ma_tham_so)
        if not obj:
            return False
        obj.delete()
        return True

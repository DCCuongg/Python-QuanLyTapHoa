# models/tham_so_luong.py
from django.db import models

class ThamSoLuong(models.Model):
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
        managed = False

    def __str__(self):
        return self.ten_tham_so


# repositories/tham_so_luong_repo.py
from typing import Optional
from django.db.models import QuerySet

class ThamSoLuongRepository:
    @staticmethod
    def get_luong_co_ban_hien_tai() -> Optional[ThamSoLuong]:
        return ThamSoLuong.objects.filter(
            ten_tham_so='LuongCoBan'
        ).order_by('-ngay_hieu_luc').first()

    @staticmethod
    def get_all() -> QuerySet[ThamSoLuong]:
        return ThamSoLuong.objects.all()

    @staticmethod
    def get_by_id(ma_tham_so: int) -> Optional[ThamSoLuong]:
        try:
            return ThamSoLuong.objects.get(pk=ma_tham_so)
        except ThamSoLuong.DoesNotExist:
            return None

    @staticmethod
    def get_by_ten(ten_tham_so: str) -> Optional[ThamSoLuong]:
        return ThamSoLuong.objects.filter(
            ten_tham_so=ten_tham_so
        ).order_by('-ngay_hieu_luc').first()

    @staticmethod
    def create(
        ten_tham_so: str,
        gia_tri_so: float = None,
        gia_tri_chu: str = None,
        ngay_hieu_luc=None,
        ghi_chu: str = None
    ) -> ThamSoLuong:
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
        obj = ThamSoLuongRepository.get_by_id(ma_tham_so)
        if not obj:
            return False
        obj.delete()
        return True

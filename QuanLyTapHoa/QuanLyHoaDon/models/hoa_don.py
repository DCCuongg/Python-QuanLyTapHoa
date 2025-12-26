# models/hoa_don.py
from django.db import models

class HoaDon(models.Model):
    ma_hd = models.AutoField(
        primary_key=True,
        db_column='MaHD'
    )

    ngay_lap = models.DateTimeField(
        db_column='NgayLap'
    )

    nhan_vien = models.ForeignKey(
        'QuanLyNhanSu.NhanVien',              # FK dùng string để tránh circular import
        on_delete=models.PROTECT,
        db_column='MaNV',
        related_name='hoa_dons'
    )

    tong_tien = models.DecimalField(
        max_digits=18,
        decimal_places=2,
        default=0,
        db_column='TongTien'
    )

    class Meta:
        db_table = 'HOA_DON'
        managed = False

    def __str__(self):
        return f"Hóa đơn #{self.ma_hd}"

# repositories/hoa_don_repo.py
from typing import Optional
from django.db.models import QuerySet
from django.utils import timezone
from decimal import Decimal

class HoaDonRepository:

    @staticmethod
    def get_all() -> QuerySet[HoaDon]:
        return HoaDon.objects.all()

    @staticmethod
    def get_by_id(ma_hd: int) -> Optional[HoaDon]:
        try:
            return HoaDon.objects.get(pk=ma_hd)
        except HoaDon.DoesNotExist:
            return None

    @staticmethod
    def get_by_nhan_vien(ma_nv: int) -> QuerySet[HoaDon]:
        return HoaDon.objects.filter(
            nhan_vien_id=ma_nv
        )

    @staticmethod
    def create(
        ma_nv: int,
        tong_tien: float = 0,
        ngay_lap=None
    ) -> HoaDon:
        obj = HoaDon(
            nhan_vien_id=ma_nv,
            tong_tien=tong_tien,
            ngay_lap=ngay_lap or timezone.now()
        )
        obj.save()
        return obj

    @staticmethod
    def update(ma_hd: int, **kwargs) -> Optional[HoaDon]:
        obj = HoaDonRepository.get_by_id(ma_hd)
        if not obj:
            return None

        for key, value in kwargs.items():
            if hasattr(obj, key):
                print(value)
                setattr(obj, key, value)


        obj.save()
        return obj

    @staticmethod
    def delete(ma_hd: int) -> bool:
        obj = HoaDonRepository.get_by_id(ma_hd)
        if not obj:
            return False
        obj.delete()
        return True

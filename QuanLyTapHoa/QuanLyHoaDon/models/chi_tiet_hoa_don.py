# models/chi_tiet_hoa_don.py
from django.db import models

class ChiTietHoaDon(models.Model):
    ma_cthd = models.AutoField(primary_key=True, db_column='MaCTHD')
    hoa_don = models.ForeignKey(
        'HoaDon',
        on_delete=models.CASCADE,
        db_column='MaHD',
        related_name='chi_tiets'
    )

    hang_hoa = models.ForeignKey(
        'QuanLyHangHoa.HangHoa',
        on_delete=models.PROTECT,
        db_column='MaHang',
        related_name='chi_tiet_hoa_dons'
    )

    so_luong = models.IntegerField(
        db_column='SoLuong'
    )

    don_gia = models.DecimalField(
        max_digits=18,
        decimal_places=2,
        db_column='DonGia'
    )

    thanh_tien = models.DecimalField(
        max_digits=18,
        decimal_places=2,
        db_column='ThanhTien',
    )

    class Meta:
        db_table = 'CHI_TIET_HOA_DON'
        managed = False
        unique_together = (('hoa_don', 'hang_hoa'),)

    def __str__(self):
        return f"HD {self.hoa_don_id} - HH {self.hang_hoa_id}"

# repositories/chi_tiet_hoa_don_repo.py
from typing import Optional
from django.db.models import QuerySet

class ChiTietHoaDonRepository:

    @staticmethod
    def get_by_hoa_don(ma_hd: int) -> QuerySet[ChiTietHoaDon]:
        return ChiTietHoaDon.objects.filter(
            hoa_don_id=ma_hd
        ).select_related('hang_hoa')

    @staticmethod
    def get(
        ma_hd: int,
        ma_hang: int
    ) -> Optional[ChiTietHoaDon]:
        try:
            return ChiTietHoaDon.objects.get(
                hoa_don_id=ma_hd,
                hang_hoa_id=ma_hang
            )
        except ChiTietHoaDon.DoesNotExist:
            return None

    @staticmethod
    def create(
        ma_hd: int,
        ma_hang: int,
        so_luong: int,
        don_gia: float
    ) -> ChiTietHoaDon:
        obj = ChiTietHoaDon(
            hoa_don_id=ma_hd,
            hang_hoa_id=ma_hang,
            so_luong=so_luong,
            don_gia=don_gia,
            thanh_tien=don_gia*so_luong,
        )
        obj.save()
        return obj

    @staticmethod
    def update(
        ma_hd: int,
        ma_hang: int,
        so_luong: int = None,
        don_gia: float = None
    ) -> Optional[ChiTietHoaDon]:
        obj = ChiTietHoaDonRepository.get(ma_hd, ma_hang)
        if not obj:
            return None

        if so_luong is not None:
            obj.so_luong = so_luong
            obj.thanh_tien = don_gia * so_luong,
        if don_gia is not None:
            obj.don_gia = don_gia
            obj.thanh_tien = don_gia * so_luong,
        obj.save()
        return obj

    @staticmethod
    def delete(ma_hd: int, ma_hang: int) -> bool:
        obj = ChiTietHoaDonRepository.get(ma_hd, ma_hang)
        if not obj:
            return False
        obj.delete()
        return True

from django.db import models
from .thuong_hieu import ThuongHieu
from .loai_hang import LoaiHang
from .don_vi_tinh import DonViTinh
from typing import List, Optional
from django.db.models import QuerySet
# =========================
# Models cho bảng HANGHOA
# =========================
class HangHoa(models.Model):
    ma_hang = models.AutoField(
        primary_key=True,
        db_column='MaHang'
    )

    ten_hang = models.CharField(
        max_length=150,
        null=False,
        db_column='TenHang'
    )

    ma_thuong_hieu = models.ForeignKey(
        'ThuongHieu',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        db_column='MaThuongHieu',
        related_name='hang_hoas'
    )

    ma_loai_hang = models.ForeignKey(
        'LoaiHang',
        on_delete=models.PROTECT,
        db_column='MaLoaiHang',
        related_name='hang_hoas'
    )

    ma_dvt = models.ForeignKey(
        'DonViTinh',
        on_delete=models.PROTECT,
        db_column='MaDVT',
        related_name='hang_hoas'
    )

    gia_nhap = models.DecimalField(
        max_digits=18,
        decimal_places=2,
        db_column='GiaNhap'
    )

    gia_ban = models.DecimalField(
        max_digits=18,
        decimal_places=2,
        db_column='GiaBan'
    )

    so_luong_ton = models.IntegerField(
        db_column='SoLuongTon'
    )

    class Meta:
        db_table = 'HANG_HOA'
        managed = False   # 🔥 BẮT BUỘC khi dùng DB có sẵn

    def __str__(self):
        return self.ten_hang

##############################################HangHoaRepository
class HangHoaRepository:

    @staticmethod
    def get_all() -> QuerySet[HangHoa]:
        """Tạm thời chính sách trả về Queryset, muốn xử lý logic python phải ép kiểu bằng list"""
        return HangHoa.objects.all()

    @staticmethod
    def get_by_id(ma_hang: int) -> Optional[HangHoa]:
        try:
            return HangHoa.objects.get(pk=ma_hang)
        except HangHoa.DoesNotExist:
            return None

    @staticmethod
    def create(
        ten_hang: str,
        ma_thuong_hieu: int = None,
        ma_loai_hang: int = None,
        ma_dvt: int = None,
        gia_nhap: float = 0,
        gia_ban: float = 0,
        so_luong_ton: int = 0
    ) -> HangHoa:
        obj = HangHoa(
            ten_hang=ten_hang,
            ma_thuong_hieu_id=ma_thuong_hieu,
            ma_loai_hang_id=ma_loai_hang,
            ma_dvt_id=ma_dvt,
            gia_nhap=gia_nhap,
            gia_ban=gia_ban,
            so_luong_ton=so_luong_ton
        )
        obj.save()
        return obj

    @staticmethod
    def update(ma_hang: int, **kwargs) -> Optional[HangHoa]:
        obj = HangHoaRepository.get_by_id(ma_hang)
        if not obj:
            return None
        for key, value in kwargs.items():
            if hasattr(obj, key):
                setattr(obj, key, value)
        obj.save()
        return obj

    @staticmethod
    def delete(ma_hang: int) -> bool:
        obj = HangHoaRepository.get_by_id(ma_hang)
        if not obj:
            return False
        obj.delete()
        return True

    @staticmethod
    def adjust_stock(ma_hang: int, so_luong: int) -> Optional[HangHoa]:
        """Cộng/trừ số lượng tồn kho"""
        obj = HangHoaRepository.get_by_id(ma_hang)
        if not obj:
            return None
        obj.so_luong_ton += so_luong
        obj.save()
        return obj
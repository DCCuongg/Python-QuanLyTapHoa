from django.db import models

# =========================
# Models cho bảng LOAIHANG
# =========================
class LoaiHang(models.Model):
    ma_loai = models.AutoField(
        primary_key=True,
        db_column="MaLoaiHang"
    )

    ten_loai = models.CharField(
        max_length=100,
        db_column="TenLoaiHang"
    )

    mo_ta = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        db_column="MoTa"
    )

    class Meta:
        db_table = "LOAI_HANG"
        managed = False   # 🔥 BẮT BUỘC – đây là thứ bạn thiếu

    def __str__(self):
        return self.ten_loai

from typing import List, Optional
class LoaiHangRepository:

    @staticmethod
    def get_all() -> List[LoaiHang]:
        return list(LoaiHang.objects.all())

    @staticmethod
    def get_by_id(ma_loai: int) -> Optional[LoaiHang]:
        try:
            return LoaiHang.objects.get(pk=ma_loai)
        except LoaiHang.DoesNotExist:
            return None

    @staticmethod
    def create(ten_loai: str, mo_ta: str = None) -> LoaiHang:
        obj = LoaiHang(ten_loai=ten_loai, mo_ta=mo_ta)
        obj.save()
        return obj

    @staticmethod
    def update(ma_loai: int, **kwargs) -> Optional[LoaiHang]:
        obj = LoaiHangRepository.get_by_id(ma_loai)
        if not obj:
            return None
        for key, value in kwargs.items():
            if hasattr(obj, key):
                setattr(obj, key, value)
        obj.save()
        return obj

    @staticmethod
    def delete(ma_loai: int) -> bool:
        obj = LoaiHangRepository.get_by_id(ma_loai)
        if not obj:
            return False
        obj.delete()
        return True
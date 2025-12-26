from django.db import models

# =========================
# Model cho bảng CHUC_VU
# =========================
class ChucVu(models.Model):
    ma_chuc_vu = models.AutoField(
        primary_key=True,
        db_column='MaChucVu'
    )

    ten_chuc_vu = models.CharField(
        max_length=50,
        null=False,
        db_column='TenChucVu'
    )

    phu_cap = models.DecimalField(
        max_digits=18,
        decimal_places=2,
        default=0,
        db_column='PhuCap'
    )

    he_so_luong = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=1,
        db_column='HeSoLuong'
    )

    ghi_chu = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        db_column='GhiChu'
    )

    class Meta:
        db_table = 'CHUC_VU'
        managed = False   # 🔥 DB có sẵn → BẮT BUỘC

    def __str__(self):
        return f"{self.ten_chuc_vu} (HS: {self.he_so_luong})"

from typing import Optional
from django.db.models import QuerySet

####################################ChucVuRepository
class ChucVuRepository:

    @staticmethod
    def get_all() -> QuerySet[ChucVu]:
        return ChucVu.objects.all()

    @staticmethod
    def get_by_id(ma_chuc_vu: int) -> Optional[ChucVu]:
        return ChucVu.objects.filter(pk=ma_chuc_vu).first()

    @staticmethod
    def create(
        ten_chuc_vu: str,
        phu_cap=0,
        he_so_luong=1,
        ghi_chu: str = None
    ) -> ChucVu:
        obj = ChucVu(
            ten_chuc_vu=ten_chuc_vu,
            phu_cap=phu_cap,
            he_so_luong=he_so_luong,
            ghi_chu=ghi_chu
        )
        obj.save()
        return obj

    @staticmethod
    def update(
        ma_chuc_vu: int,
        **kwargs
    ) -> Optional[ChucVu]:
        obj = ChucVuRepository.get_by_id(ma_chuc_vu)
        if not obj:
            return None

        for field in ['ten_chuc_vu', 'phu_cap', 'he_so_luong', 'ghi_chu']:
            if field in kwargs:
                setattr(obj, field, kwargs[field])

        obj.save()
        return obj

    @staticmethod
    def delete(ma_chuc_vu: int) -> bool:
        obj = ChucVuRepository.get_by_id(ma_chuc_vu)
        if not obj:
            return False
        obj.delete()
        return True

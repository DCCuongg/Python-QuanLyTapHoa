from django.db import models

# =========================
# Models cho bảng THUONGHIEU
# =========================
class ThuongHieu(models.Model):
    ma_thuong_hieu = models.AutoField(primary_key=True)  # tương đương INT IDENTITY(1,1)
    ten_thuong_hieu = models.CharField(max_length=100, null=False)
    quoc_gia = models.CharField(max_length=100, null=True, blank=True)
    mo_ta = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        db_table = 'THUONG_HIEU'  # giữ tên bảng giống SQL Server

    def __str__(self):
        return self.ten_thuong_hieu

# =========================
from typing import List, Optional
class ThuongHieuRepository:

    @staticmethod
    def get_all() -> List[ThuongHieu]:
        return list(ThuongHieu.objects.all())

    @staticmethod
    def get_by_id(ma_thuong_hieu: int) -> Optional[ThuongHieu]:
        try:
            return ThuongHieu.objects.get(pk=ma_thuong_hieu)
        except ThuongHieu.DoesNotExist:
            return None

    @staticmethod
    def create(ten_thuong_hieu: str, quoc_gia: str = None, mo_ta: str = None) -> ThuongHieu:
        obj = ThuongHieu(
            ten_thuong_hieu=ten_thuong_hieu,
            quoc_gia=quoc_gia,
            mo_ta=mo_ta
        )
        obj.save()
        return obj

    @staticmethod
    def update(ma_thuong_hieu: int, **kwargs) -> Optional[ThuongHieu]:
        obj = ThuongHieuRepository.get_by_id(ma_thuong_hieu)
        if not obj:
            return None
        for key, value in kwargs.items():
            if hasattr(obj, key):
                setattr(obj, key, value)
        obj.save()
        return obj

    @staticmethod
    def delete(ma_thuong_hieu: int) -> bool:
        obj = ThuongHieuRepository.get_by_id(ma_thuong_hieu)
        if not obj:
            return False
        obj.delete()
        return True
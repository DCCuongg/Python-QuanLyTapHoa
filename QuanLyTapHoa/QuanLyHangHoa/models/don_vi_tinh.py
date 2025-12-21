from django.db import models
# =========================
# Models cho bảng DONVITINH
# =========================
class DonViTinh(models.Model):
    ma_dvt = models.AutoField(
        primary_key=True,
        db_column='MaDVT'
    )

    ten_dvt = models.CharField(
        max_length=50,
        db_column='TenDVT'
    )

    class Meta:
        db_table = 'DON_VI_TINH'
        managed = False  # ⚠️ Bắt buộc khi dùng DB restore sẵn

    def __str__(self):
        return self.ten_dvt


from typing import List, Optional
class DonViTinhRepository:

    @staticmethod
    def get_all() -> List[DonViTinh]:
        return list(DonViTinh.objects.all())

    @staticmethod
    def get_by_id(ma_dvt: int) -> Optional[DonViTinh]:
        try:
            return DonViTinh.objects.get(pk=ma_dvt)
        except DonViTinh.DoesNotExist:
            return None

    @staticmethod
    def create(ten_dvt: str) -> DonViTinh:
        obj = DonViTinh(ten_dvt=ten_dvt)
        obj.save()
        return obj

    @staticmethod
    def update(ma_dvt: int, ten_dvt: str) -> Optional[DonViTinh]:
        obj = DonViTinhRepository.get_by_id(ma_dvt)
        if not obj:
            return None
        obj.ten_dvt = ten_dvt
        obj.save()
        return obj

    @staticmethod
    def delete(ma_dvt: int) -> bool:
        obj = DonViTinhRepository.get_by_id(ma_dvt)
        if not obj:
            return False
        obj.delete()
        return True
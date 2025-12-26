from django.db import models

# =========================
# Model cho bảng NHAN_VIEN
# =========================
class NhanVien(models.Model):
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
        'ChucVu',                 # dùng string reference
        on_delete=models.PROTECT, # DB có FK → không cho xóa chức vụ đang dùng
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
        managed = False   # 🔥 DB có sẵn

    def __str__(self):
        return f"{self.ho_ten} (#{self.ma_nv})"

####################NhanVienRepository
from typing import Optional
from django.db.models import QuerySet


class NhanVienRepository:

    @staticmethod
    def get_all() -> QuerySet[NhanVien]:
        return NhanVien.objects.select_related('ma_chuc_vu')

    @staticmethod
    def get_by_id(ma_nv: int) -> Optional[NhanVien]:
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
        obj = NhanVien(
            ho_ten=ho_ten,
            ma_chuc_vu_id=ma_chuc_vu,  # 👈 gán ID (repo style)
            sdt=sdt,
            dia_chi=dia_chi
        )
        obj.save()
        return obj

    @staticmethod
    def update(ma_nv: int, **kwargs) -> Optional[NhanVien]:
        obj = NhanVienRepository.get_by_id(ma_nv)
        if not obj:
            return None

        for field in ['ho_ten', 'ma_chuc_vu', 'sdt', 'dia_chi']:
            if field in kwargs:
                setattr(obj, field, kwargs[field])

        obj.save()
        return obj

    @staticmethod
    def delete(ma_nv: int) -> bool:
        obj = NhanVienRepository.get_by_id(ma_nv)
        if not obj:
            return False
        obj.delete()
        return True

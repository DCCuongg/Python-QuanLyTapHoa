from django.db import models
from typing import Optional
from django.db.models import QuerySet

# =========================
# Model cho bảng CHUC_VU
# =========================
class ChucVu(models.Model):
    """
    Model ánh xạ bảng CHUC_VU trong cơ sở dữ liệu.

    Lưu thông tin chức vụ của nhân viên, bao gồm:
    - Tên chức vụ
    - Phụ cấp
    - Hệ số lương
    - Ghi chú (nếu có)

    Bảng này là bảng có sẵn trong CSDL nên managed = False.
    """

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
        managed = False  # DB có sẵn → không để Django tự migrate

    def __str__(self):
        return f"{self.ten_chuc_vu} (HS: {self.he_so_luong})"


# =========================
# Repository cho ChucVu
# =========================
class ChucVuRepository:
    """
    Repository xử lý toàn bộ thao tác CRUD cho bảng CHUC_VU.

    Lớp này đóng vai trò trung gian giữa Service/View và Model,
    giúp:
    - Tránh gọi ORM trực tiếp trong View
    - Dễ bảo trì, mở rộng nghiệp vụ
    """

    @staticmethod
    def get_all() -> QuerySet[ChucVu]:
        """
        Lấy danh sách tất cả chức vụ.

        :return: QuerySet[ChucVu]
        """
        return ChucVu.objects.all()

    @staticmethod
    def get_by_id(ma_chuc_vu: int) -> Optional[ChucVu]:
        """
        Lấy chức vụ theo mã chức vụ.

        :param ma_chuc_vu: Mã chức vụ
        :return: ChucVu hoặc None nếu không tồn tại
        """
        return ChucVu.objects.filter(pk=ma_chuc_vu).first()

    @staticmethod
    def create(
        ten_chuc_vu: str,
        phu_cap=0,
        he_so_luong=1,
        ghi_chu: str = None
    ) -> ChucVu:
        """
        Tạo mới một chức vụ.

        :param ten_chuc_vu: Tên chức vụ
        :param phu_cap: Phụ cấp (mặc định = 0)
        :param he_so_luong: Hệ số lương (mặc định = 1)
        :param ghi_chu: Ghi chú (tùy chọn)
        :return: Đối tượng ChucVu đã được tạo
        """
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
        """
        Cập nhật thông tin chức vụ.

        :param ma_chuc_vu: Mã chức vụ cần cập nhật
        :param kwargs: Các field được phép cập nhật
        :return: ChucVu sau khi cập nhật hoặc None nếu không tồn tại
        """
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
        """
        Xóa chức vụ theo mã chức vụ.

        :param ma_chuc_vu: Mã chức vụ
        :return: True nếu xóa thành công, False nếu không tồn tại
        """
        obj = ChucVuRepository.get_by_id(ma_chuc_vu)
        if not obj:
            return False
        obj.delete()
        return True

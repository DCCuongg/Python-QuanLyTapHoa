from django.db import models

# =========================
# Models cho bảng THUONGHIEU
# =========================
class ThuongHieu(models.Model):
    """
    Lớp Model biểu diễn thực thể Thương Hiệu,
    dùng để lưu trữ thông tin thương hiệu của hàng hóa trong hệ thống.
    """

    ma_thuong_hieu = models.AutoField(
        primary_key=True,
        db_column='MaThuongHieu'
    )

    ten_thuong_hieu = models.CharField(
        max_length=100,
        db_column='TenThuongHieu'
    )

    quoc_gia = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        db_column='QuocGia'
    )

    mo_ta = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        db_column='MoTa'
    )

    class Meta:
        db_table = 'THUONG_HIEU'
        managed = False  # ⚠️ Bắt buộc khi dùng DB có sẵn

    def __str__(self):
        """
        Trả về tên thương hiệu khi hiển thị đối tượng.

        Returns:
            str: Tên thương hiệu.
        """
        return self.ten_thuong_hieu


# =========================
from typing import List, Optional

class ThuongHieuRepository:
    """
    Lớp Repository chịu trách nhiệm truy xuất và thao tác dữ liệu
    liên quan đến bảng Thương Hiệu trong cơ sở dữ liệu.
    """

    @staticmethod
    def get_all() -> List[ThuongHieu]:
        """
        Lấy danh sách tất cả thương hiệu trong hệ thống.

        Returns:
            List[ThuongHieu]: Danh sách các đối tượng thương hiệu.
        """
        return list(ThuongHieu.objects.all())

    @staticmethod
    def get_by_id(ma_thuong_hieu: int) -> Optional[ThuongHieu]:
        """
        Lấy thông tin thương hiệu theo mã thương hiệu.

        Args:
            ma_thuong_hieu (int): Mã định danh của thương hiệu.

        Returns:
            ThuongHieu | None: Đối tượng thương hiệu nếu tồn tại,
            ngược lại trả về None.
        """
        try:
            return ThuongHieu.objects.get(pk=ma_thuong_hieu)
        except ThuongHieu.DoesNotExist:
            return None

    @staticmethod
    def create(
        ten_thuong_hieu: str,
        quoc_gia: str = None,
        mo_ta: str = None
    ) -> ThuongHieu:
        """
        Tạo mới một thương hiệu.

        Args:
            ten_thuong_hieu (str): Tên thương hiệu.
            quoc_gia (str, optional): Quốc gia của thương hiệu.
            mo_ta (str, optional): Mô tả thương hiệu.

        Returns:
            ThuongHieu: Đối tượng thương hiệu vừa được tạo.
        """
        obj = ThuongHieu(
            ten_thuong_hieu=ten_thuong_hieu,
            quoc_gia=quoc_gia,
            mo_ta=mo_ta
        )
        obj.save()
        return obj

    @staticmethod
    def update(ma_thuong_hieu: int, **kwargs) -> Optional[ThuongHieu]:
        """
        Cập nhật thông tin thương hiệu theo mã thương hiệu.

        Args:
            ma_thuong_hieu (int): Mã định danh của thương hiệu cần cập nhật.
            **kwargs: Các trường cần cập nhật và giá trị tương ứng.

        Returns:
            ThuongHieu | None: Đối tượng thương hiệu sau khi cập nhật,
            hoặc None nếu không tồn tại.
        """
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
        """
        Xóa một thương hiệu theo mã thương hiệu.

        Args:
            ma_thuong_hieu (int): Mã định danh của thương hiệu cần xóa.

        Returns:
            bool: True nếu xóa thành công, False nếu không tồn tại.
        """
        obj = ThuongHieuRepository.get_by_id(ma_thuong_hieu)
        if not obj:
            return False
        obj.delete()
        return True

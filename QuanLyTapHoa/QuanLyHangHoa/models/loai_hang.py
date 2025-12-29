from django.db import models

# =========================
# Models cho bảng LOAIHANG
# =========================
class LoaiHang(models.Model):
    """
    Lớp Model biểu diễn thực thể Loại Hàng,
    dùng để phân loại các hàng hóa trong hệ thống.
    """

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
        """
        Trả về tên loại hàng khi hiển thị đối tượng.

        Returns:
            str: Tên loại hàng.
        """
        return self.ten_loai


from typing import List, Optional

class LoaiHangRepository:
    """
    Lớp Repository chịu trách nhiệm truy xuất và thao tác dữ liệu
    liên quan đến bảng Loại Hàng trong cơ sở dữ liệu.
    """

    @staticmethod
    def get_all() -> List[LoaiHang]:
        """
        Lấy danh sách tất cả loại hàng trong hệ thống.

        Returns:
            List[LoaiHang]: Danh sách các đối tượng loại hàng.
        """
        return list(LoaiHang.objects.all())

    @staticmethod
    def get_by_id(ma_loai: int) -> Optional[LoaiHang]:
        """
        Lấy thông tin loại hàng theo mã loại hàng.

        Args:
            ma_loai (int): Mã định danh của loại hàng.

        Returns:
            LoaiHang | None: Đối tượng loại hàng nếu tồn tại,
            ngược lại trả về None.
        """
        try:
            return LoaiHang.objects.get(pk=ma_loai)
        except LoaiHang.DoesNotExist:
            return None

    @staticmethod
    def create(ten_loai: str, mo_ta: str = None) -> LoaiHang:
        """
        Tạo mới một loại hàng.

        Args:
            ten_loai (str): Tên loại hàng.
            mo_ta (str, optional): Mô tả loại hàng.

        Returns:
            LoaiHang: Đối tượng loại hàng vừa được tạo.
        """
        obj = LoaiHang(ten_loai=ten_loai, mo_ta=mo_ta)
        obj.save()
        return obj

    @staticmethod
    def update(ma_loai: int, **kwargs) -> Optional[LoaiHang]:
        """
        Cập nhật thông tin loại hàng theo mã loại hàng.

        Args:
            ma_loai (int): Mã định danh của loại hàng cần cập nhật.
            **kwargs: Các trường cần cập nhật và giá trị tương ứng.

        Returns:
            LoaiHang | None: Đối tượng loại hàng sau khi cập nhật,
            hoặc None nếu không tồn tại.
        """
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
        """
        Xóa một loại hàng theo mã loại hàng.

        Args:
            ma_loai (int): Mã định danh của loại hàng cần xóa.

        Returns:
            bool: True nếu xóa thành công, False nếu không tồn tại.
        """
        obj = LoaiHangRepository.get_by_id(ma_loai)
        if not obj:
            return False
        obj.delete()
        return True

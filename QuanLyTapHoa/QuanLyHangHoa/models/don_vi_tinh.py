from django.db import models

# =========================
# Models cho bảng DONVITINH
# =========================
class DonViTinh(models.Model):
    """
    Lớp Model biểu diễn thực thể Đơn Vị Tính,
    dùng để lưu trữ thông tin đơn vị đo lường của hàng hóa trong hệ thống.
    """

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
        """
        Trả về tên đơn vị tính khi hiển thị đối tượng.

        Returns:
            str: Tên đơn vị tính.
        """
        return self.ten_dvt

from typing import List, Optional

class DonViTinhRepository:
    """
    Lớp Repository chịu trách nhiệm truy xuất và thao tác dữ liệu
    liên quan đến bảng Đơn Vị Tính trong cơ sở dữ liệu.
    """

    @staticmethod
    def get_all() -> List[DonViTinh]:
        """
        Lấy danh sách tất cả đơn vị tính trong hệ thống.

        Returns:
            List[DonViTinh]: Danh sách các đối tượng đơn vị tính.
        """
        return list(DonViTinh.objects.all())

    @staticmethod
    def get_by_id(ma_dvt: int) -> Optional[DonViTinh]:
        """
        Lấy thông tin đơn vị tính theo mã đơn vị tính.

        Args:
            ma_dvt (int): Mã định danh của đơn vị tính.

        Returns:
            DonViTinh | None: Đối tượng đơn vị tính nếu tồn tại,
            ngược lại trả về None.
        """
        try:
            return DonViTinh.objects.get(pk=ma_dvt)
        except DonViTinh.DoesNotExist:
            return None

    @staticmethod
    def create(ten_dvt: str) -> DonViTinh:
        """
        Tạo mới một đơn vị tính.

        Args:
            ten_dvt (str): Tên đơn vị tính cần tạo.

        Returns:
            DonViTinh: Đối tượng đơn vị tính vừa được tạo.
        """
        obj = DonViTinh(ten_dvt=ten_dvt)
        obj.save()
        return obj

    @staticmethod
    def update(ma_dvt: int, ten_dvt: str) -> Optional[DonViTinh]:
        """
        Cập nhật tên đơn vị tính theo mã đơn vị tính.

        Args:
            ma_dvt (int): Mã định danh của đơn vị tính cần cập nhật.
            ten_dvt (str): Tên đơn vị tính mới.

        Returns:
            DonViTinh | None: Đối tượng đơn vị tính sau khi cập nhật,
            hoặc None nếu không tồn tại.
        """
        obj = DonViTinhRepository.get_by_id(ma_dvt)
        if not obj:
            return None
        obj.ten_dvt = ten_dvt
        obj.save()
        return obj

    @staticmethod
    def delete(ma_dvt: int) -> bool:
        """
        Xóa một đơn vị tính theo mã đơn vị tính.

        Args:
            ma_dvt (int): Mã định danh của đơn vị tính cần xóa.

        Returns:
            bool: True nếu xóa thành công, False nếu không tồn tại.
        """
        obj = DonViTinhRepository.get_by_id(ma_dvt)
        if not obj:
            return False
        obj.delete()
        return True

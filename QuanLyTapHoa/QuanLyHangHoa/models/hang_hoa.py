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
    """
    Lớp Model biểu diễn thực thể Hàng Hóa,
    dùng để lưu trữ thông tin hàng hóa trong hệ thống quản lý tạp hóa.
    """

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
        """
        Trả về tên hàng hóa khi hiển thị đối tượng.

        Returns:
            str: Tên hàng hóa.
        """
        return self.ten_hang


##############################################
# HangHoaRepository
##############################################
class HangHoaRepository:
    """
    Lớp Repository chịu trách nhiệm truy xuất và thao tác dữ liệu
    liên quan đến bảng Hàng Hóa trong cơ sở dữ liệu.
    """

    @staticmethod
    def get_all() -> QuerySet[HangHoa]:
        """
        Lấy danh sách tất cả hàng hóa trong hệ thống.

        Returns:
            QuerySet[HangHoa]: Danh sách hàng hóa dưới dạng QuerySet.
        """
        return HangHoa.objects.all()

    @staticmethod
    def get_by_id(ma_hang: int) -> Optional[HangHoa]:
        """
        Lấy thông tin hàng hóa theo mã hàng.

        Args:
            ma_hang (int): Mã định danh của hàng hóa.

        Returns:
            HangHoa | None: Đối tượng hàng hóa nếu tồn tại,
            ngược lại trả về None.
        """
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
        """
        Tạo mới một hàng hóa.

        Args:
            ten_hang (str): Tên hàng hóa.
            ma_thuong_hieu (int, optional): Mã thương hiệu.
            ma_loai_hang (int, optional): Mã loại hàng.
            ma_dvt (int, optional): Mã đơn vị tính.
            gia_nhap (float): Giá nhập hàng hóa.
            gia_ban (float): Giá bán hàng hóa.
            so_luong_ton (int): Số lượng tồn kho ban đầu.

        Returns:
            HangHoa: Đối tượng hàng hóa vừa được tạo.
        """
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
        """
        Cập nhật thông tin hàng hóa theo mã hàng.

        Args:
            ma_hang (int): Mã định danh của hàng hóa cần cập nhật.
            **kwargs: Các trường cần cập nhật và giá trị tương ứng.

        Returns:
            HangHoa | None: Đối tượng hàng hóa sau khi cập nhật,
            hoặc None nếu không tồn tại.
        """
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
        """
        Xóa một hàng hóa theo mã hàng.

        Args:
            ma_hang (int): Mã định danh của hàng hóa cần xóa.

        Returns:
            bool: True nếu xóa thành công, False nếu không tồn tại.
        """
        obj = HangHoaRepository.get_by_id(ma_hang)
        if not obj:
            return False
        obj.delete()
        return True

    @staticmethod
    def adjust_stock(ma_hang: int, so_luong: int) -> Optional[HangHoa]:
        """
        Điều chỉnh số lượng tồn kho của hàng hóa (cộng hoặc trừ).

        Args:
            ma_hang (int): Mã định danh của hàng hóa.
            so_luong (int): Số lượng cần điều chỉnh (dương hoặc âm).

        Returns:
            HangHoa | None: Đối tượng hàng hóa sau khi cập nhật tồn kho,
            hoặc None nếu không tồn tại.
        """
        obj = HangHoaRepository.get_by_id(ma_hang)
        if not obj:
            return None
        obj.so_luong_ton += so_luong
        obj.save()
        return obj

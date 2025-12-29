# models/hoa_don.py
from django.db import models
from django.db.models import Count, Sum
from django.db.models.functions import ExtractMonth
"""
Model HoaDon

Định nghĩa model HoaDon tương ứng với bảng HOA_DON trong cơ sở dữ liệu.
Lưu thông tin hóa đơn bán hàng, nhân viên lập hóa đơn và tổng tiền.
"""

from django.db import models
from django.db.models import Count, Sum
from django.db.models.functions import ExtractMonth


class HoaDon(models.Model):
    """
    Model đại diện cho hóa đơn bán hàng.
    """

    ma_hd = models.AutoField(
        primary_key=True,
        db_column='MaHD'
    )

    ngay_lap = models.DateTimeField(
        db_column='NgayLap'
    )

    nhan_vien = models.ForeignKey(
        'QuanLyNhanSu.NhanVien',
        on_delete=models.PROTECT,
        db_column='MaNV',
        related_name='hoa_dons'
    )

    tong_tien = models.DecimalField(
        max_digits=18,
        decimal_places=2,
        default=0,
        db_column='TongTien'
    )

    class Meta:
        """
        Cấu hình ánh xạ model với bảng CSDL.
        """
        db_table = 'HOA_DON'
        managed = False

    def __str__(self):
        """
        Hiển thị chuỗi đại diện của hóa đơn.
        """
        return f"Hóa đơn #{self.ma_hd}"


"""
HoaDonRepository

Cung cấp các phương thức thao tác dữ liệu cho model HoaDon.
Bao gồm CRUD và các truy vấn thống kê.
"""
from typing import Optional
from django.db.models import QuerySet
from django.utils import timezone
from decimal import Decimal

from QuanLyHoaDon.models.hoa_don import HoaDon

class HoaDonRepository:
    """
    Repository xử lý truy vấn và thao tác dữ liệu liên quan đến HoaDon.
    """

    @staticmethod
    def get_all() -> QuerySet[HoaDon]:
        """
        Lấy danh sách tất cả hóa đơn.
        """
        return HoaDon.objects.all()

    @staticmethod
    def get_by_id(ma_hd: int) -> Optional[HoaDon]:
        """
        Lấy hóa đơn theo mã hóa đơn.

        :param ma_hd: Mã hóa đơn
        :return: HoaDon hoặc None nếu không tồn tại
        """
        try:
            return HoaDon.objects.get(pk=ma_hd)
        except HoaDon.DoesNotExist:
            return None

    @staticmethod
    def get_by_nhan_vien(ma_nv: int) -> QuerySet[HoaDon]:
        """
        Lấy danh sách hóa đơn theo nhân viên.
        """
        return HoaDon.objects.filter(
            nhan_vien_id=ma_nv
        )

    @staticmethod
    def create(
            ma_nv: int,
            tong_tien: float = 0,
            ngay_lap=None
    ) -> HoaDon:
        """
        Tạo mới hóa đơn.

        :param ma_nv: Mã nhân viên
        :param tong_tien: Tổng tiền ban đầu
        :param ngay_lap: Ngày lập hóa đơn
        """
        obj = HoaDon(
            nhan_vien_id=ma_nv,
            tong_tien=tong_tien,
            ngay_lap=ngay_lap or timezone.now()
        )
        obj.save()
        return obj

    @staticmethod
    def update(ma_hd: int, **kwargs) -> Optional[HoaDon]:
        """
        Cập nhật thông tin hóa đơn.

        :param ma_hd: Mã hóa đơn
        :param kwargs: Các trường cần cập nhật
        """
        obj = HoaDonRepository.get_by_id(ma_hd)
        if not obj:
            return None

        for key, value in kwargs.items():
            if hasattr(obj, key):
                setattr(obj, key, value)

        obj.save()
        return obj

    @staticmethod
    def delete(ma_hd: int) -> bool:
        """
        Xóa hóa đơn theo mã hóa đơn.
        """
        obj = HoaDonRepository.get_by_id(ma_hd)
        if not obj:
            return False
        obj.delete()
        return True

    @staticmethod
    def thong_ke_theo_nhan_vien():
        """
        Thống kê số hóa đơn và tổng doanh thu theo nhân viên.
        """
        return (
            HoaDon.objects
            .values(
                'nhan_vien_id',
                'nhan_vien__ho_ten'
            )
            .annotate(
                so_hoa_don=Count('ma_hd'),
                tong_doanh_thu=Sum('tong_tien')
            )
            .order_by('nhan_vien_id')
        )

    @staticmethod
    def thong_ke_doanh_thu_theo_nam(nam: int):
        """
        Thống kê doanh thu theo từng tháng trong năm.

        :param nam: Năm cần thống kê
        """
        return (
            HoaDon.objects
            .filter(ngay_lap__year=nam)
            .annotate(thang=ExtractMonth('ngay_lap'))
            .values('thang')
            .annotate(tong_doanh_thu=Sum('tong_tien'))
            .order_by('thang')
        )

# models/chi_tiet_hoa_don.py
from django.db import models
# models/chi_tiet_hoa_don.py
from django.db import models

class ChiTietHoaDon(models.Model):
    """
    Model ChiTietHoaDon đại diện cho bảng CHI_TIET_HOA_DON trong CSDL.

    Mỗi bản ghi thể hiện một mặt hàng cụ thể trong một hóa đơn,
    bao gồm số lượng, đơn giá và thành tiền.

    Quan hệ:
    - Many-to-One với HoaDon
    - Many-to-One với HangHoa

    Ràng buộc:
    - Mỗi cặp (hoa_don, hang_hoa) là duy nhất.
    """

    ma_cthd = models.AutoField(primary_key=True, db_column='MaCTHD')

    hoa_don = models.ForeignKey(
        'HoaDon',
        on_delete=models.CASCADE,
        db_column='MaHD',
        related_name='chi_tiets'
    )

    hang_hoa = models.ForeignKey(
        'QuanLyHangHoa.HangHoa',
        on_delete=models.PROTECT,
        db_column='MaHang',
        related_name='chi_tiet_hoa_dons'
    )

    so_luong = models.IntegerField(
        db_column='SoLuong'
    )

    don_gia = models.DecimalField(
        max_digits=18,
        decimal_places=2,
        db_column='DonGia'
    )

    thanh_tien = models.DecimalField(
        max_digits=18,
        decimal_places=2,
        db_column='ThanhTien',
    )

    class Meta:
        """
        Cấu hình ánh xạ model với bảng trong cơ sở dữ liệu.
        """
        db_table = 'CHI_TIET_HOA_DON'
        managed = False
        unique_together = (('hoa_don', 'hang_hoa'),)

    def __str__(self):
        """
        Chuỗi hiển thị phục vụ debug và admin.
        """
        return f"HD {self.hoa_don_id} - HH {self.hang_hoa_id}"
# repositories/chi_tiet_hoa_don_repo.py
from typing import Optional
from django.db.models import QuerySet

class ChiTietHoaDonRepository:
    """
    Repository xử lý truy vấn và thao tác dữ liệu cho ChiTietHoaDon.

    Lớp này đóng vai trò trung gian giữa Service và ORM,
    giúp tách biệt nghiệp vụ và truy cập dữ liệu.
    """

    @staticmethod
    def get_by_hoa_don(ma_hd: int) -> QuerySet[ChiTietHoaDon]:
        """
        Lấy danh sách chi tiết hóa đơn theo mã hóa đơn.

        :param ma_hd: Mã hóa đơn
        :return: QuerySet các ChiTietHoaDon thuộc hóa đơn
        """
        return ChiTietHoaDon.objects.filter(
            hoa_don_id=ma_hd
        ).select_related('hang_hoa')

    @staticmethod
    def get(
        ma_hd: int,
        ma_hang: int
    ) -> Optional[ChiTietHoaDon]:
        """
        Lấy một chi tiết hóa đơn theo mã hóa đơn và mã hàng hóa.

        :param ma_hd: Mã hóa đơn
        :param ma_hang: Mã hàng hóa
        :return: Đối tượng ChiTietHoaDon hoặc None nếu không tồn tại
        """
        try:
            return ChiTietHoaDon.objects.get(
                hoa_don_id=ma_hd,
                hang_hoa_id=ma_hang
            )
        except ChiTietHoaDon.DoesNotExist:
            return None

    @staticmethod
    def create(
        ma_hd: int,
        ma_hang: int,
        so_luong: int,
        don_gia: float
    ) -> ChiTietHoaDon:
        """
        Tạo mới một chi tiết hóa đơn.

        :param ma_hd: Mã hóa đơn
        :param ma_hang: Mã hàng hóa
        :param so_luong: Số lượng mua
        :param don_gia: Đơn giá tại thời điểm bán
        :return: Đối tượng ChiTietHoaDon vừa tạo
        """
        obj = ChiTietHoaDon(
            hoa_don_id=ma_hd,
            hang_hoa_id=ma_hang,
            so_luong=so_luong,
            don_gia=don_gia,
            thanh_tien=don_gia * so_luong,
        )
        obj.save()
        return obj

    @staticmethod
    def update(
        ma_hd: int,
        ma_hang: int,
        so_luong: int = None,
        don_gia: float = None
    ) -> Optional[ChiTietHoaDon]:
        """
        Cập nhật số lượng hoặc đơn giá của chi tiết hóa đơn.

        :param ma_hd: Mã hóa đơn
        :param ma_hang: Mã hàng hóa
        :param so_luong: Số lượng mới (nếu có)
        :param don_gia: Đơn giá mới (nếu có)
        :return: Đối tượng ChiTietHoaDon sau khi cập nhật hoặc None
        """
        obj = ChiTietHoaDonRepository.get(ma_hd, ma_hang)
        if not obj:
            return None

        if so_luong is not None:
            obj.so_luong = so_luong

        if don_gia is not None:
            obj.don_gia = don_gia

        if so_luong is not None or don_gia is not None:
            obj.thanh_tien = obj.so_luong * obj.don_gia

        obj.save()
        return obj

    @staticmethod
    def delete(ma_hd: int, ma_hang: int) -> bool:
        """
        Xóa một chi tiết hóa đơn.

        :param ma_hd: Mã hóa đơn
        :param ma_hang: Mã hàng hóa
        :return: True nếu xóa thành công, False nếu không tồn tại
        """
        obj = ChiTietHoaDonRepository.get(ma_hd, ma_hang)
        if not obj:
            return False
        obj.delete()
        return True

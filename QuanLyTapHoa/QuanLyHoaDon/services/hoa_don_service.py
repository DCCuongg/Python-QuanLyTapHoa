# services/hoa_don_service.py
"""
Service layer cho nghiệp vụ Hóa Đơn.

Chịu trách nhiệm:
- Xử lý nghiệp vụ tạo hóa đơn
- Kiểm tra tồn kho
- Trừ tồn kho hàng hóa
- Tính tổng tiền hóa đơn
- Gọi Repository để thao tác dữ liệu

Service KHÔNG làm việc trực tiếp với request/response.
"""

from typing import Dict
from django.db import transaction
from django.utils import timezone
from django.db.models import QuerySet
from decimal import Decimal

from QuanLyHoaDon.models.hoa_don import HoaDonRepository
from QuanLyHoaDon.models.hoa_don import HoaDon
from QuanLyHoaDon.models.chi_tiet_hoa_don import ChiTietHoaDonRepository
from QuanLyHangHoa.services.hang_hoa_service import HangHoaService
from QuanLyHangHoa.models.hang_hoa import HangHoa


class HoaDonService:
    """
    Service xử lý toàn bộ nghiệp vụ liên quan đến Hóa Đơn.
    """

    @staticmethod
    @transaction.atomic
    def create_hoa_don(validated_data: Dict):
        """
        Tạo mới hóa đơn và các chi tiết hóa đơn.

        Quy trình:
        1. Kiểm tra tồn kho cho từng hàng hóa
        2. Tạo hóa đơn
        3. Tạo chi tiết hóa đơn
        4. Trừ tồn kho hàng hóa
        5. Tính và cập nhật tổng tiền

        Args:
            validated_data (Dict): dữ liệu đã được HoaDonSerializer validate

        Raises:
            ValueError: nếu tồn kho không đủ

        Returns:
            HoaDon: hóa đơn vừa tạo
        """

        chi_tiet_hoa_dons = validated_data.pop("chi_tiets")
        nhan_vien = validated_data["nhan_vien"]

        # Kiểm tra tồn kho trước khi tạo hóa đơn
        for ct in chi_tiet_hoa_dons:
            hang_hoa: HangHoa = ct["hang_hoa"]
            so_luong = ct["so_luong"]

            if hang_hoa.so_luong_ton < so_luong:
                raise ValueError(
                    f"Hàng '{hang_hoa.ten_hang}' không đủ tồn kho"
                )

        # Tạo hóa đơn
        hoa_don = HoaDonRepository.create(
            ma_nv=nhan_vien.ma_nv,
            ngay_lap=timezone.now(),
            tong_tien=0
        )

        tong_tien = Decimal(0)

        # Tạo chi tiết hóa đơn và trừ tồn kho
        for ct in chi_tiet_hoa_dons:
            hang_hoa: HangHoa = ct["hang_hoa"]
            so_luong = ct["so_luong"]
            don_gia = ct.get("don_gia", hang_hoa.gia_ban)

            # Trừ tồn kho
            HangHoaService.adjust_stock(
                ma_hang=hang_hoa.ma_hang,
                so_luong=-so_luong
            )

            thanh_tien = Decimal(so_luong) * Decimal(don_gia)
            tong_tien += thanh_tien

            ChiTietHoaDonRepository.create(
                ma_hd=hoa_don.ma_hd,
                ma_hang=hang_hoa.ma_hang,
                so_luong=so_luong,
                don_gia=don_gia
            )

        # Cập nhật tổng tiền hóa đơn
        HoaDonRepository.update(
            hoa_don.ma_hd,
            **{"tong_tien": tong_tien}
        )

        return HoaDonRepository.get_by_id(hoa_don.ma_hd)

    @staticmethod
    def get_all_hoa_don() -> QuerySet[HoaDon]:
        """
        Lấy danh sách toàn bộ hóa đơn.

        Returns:
            QuerySet[HoaDon]: danh sách hóa đơn (lazy loading)
        """
        return HoaDonRepository.get_all()

    @staticmethod
    def get_hoa_don_by_nhan_vien(ma_nv: int) -> QuerySet[HoaDon]:
        """
        Lấy danh sách hóa đơn theo nhân viên.

        Args:
            ma_nv (int): mã nhân viên

        Returns:
            QuerySet[HoaDon]: danh sách hóa đơn
        """
        return HoaDonRepository.get_by_nhan_vien(ma_nv)

    @staticmethod
    def doanh_thu_theo_thang(nam: int):
        """
        Thống kê doanh thu theo từng tháng trong năm.

        Đảm bảo luôn trả về đủ 12 tháng,
        tháng không có dữ liệu sẽ có doanh thu = 0.

        Args:
            nam (int): năm cần thống kê

        Returns:
            list[dict]: danh sách doanh thu theo tháng
        """

        raw_data = HoaDonRepository.thong_ke_doanh_thu_theo_nam(nam)

        doanh_thu_map = {
            item["thang"]: item["tong_doanh_thu"]
            for item in raw_data
        }

        result = []
        for thang in range(1, 13):
            result.append({
                "thang": thang,
                "tong_doanh_thu": doanh_thu_map.get(thang, Decimal(0))
            })

        return result

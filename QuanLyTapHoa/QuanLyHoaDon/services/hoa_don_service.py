# services/hoa_don_service.py
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

    @staticmethod
    @transaction.atomic
    def create_hoa_don(validated_data: Dict):
        """
        validated_data đã được HoaDonSerializer validate
        """

        chi_tiet_hoa_dons = validated_data.pop("chi_tiets")
        nhan_vien = validated_data["nhan_vien"]

        # 1️⃣ Kiểm tra tồn kho trước
        for ct in chi_tiet_hoa_dons:
            hang_hoa: HangHoa = ct["hang_hoa"]
            so_luong = ct["so_luong"]

            if hang_hoa.so_luong_ton < so_luong:
                raise ValueError(
                    f"Hàng '{hang_hoa.ten_hang}' không đủ tồn kho"
                )

        # 2️⃣ Tạo hóa đơn
        hoa_don = HoaDonRepository.create(
            ma_nv=nhan_vien.ma_nv,
            ngay_lap=timezone.now(),
            tong_tien=0
        )

        tongtien = 0

        # 3️⃣ Tạo chi tiết + trừ kho
        for ct in chi_tiet_hoa_dons:
            hang_hoa: HangHoa = ct["hang_hoa"]
            so_luong = ct["so_luong"]
            don_gia = ct.get("don_gia", hang_hoa.gia_ban)  # lấy giá bán nếu không có giá cụ thể

            # trừ tồn kho → GỌI SERVICE
            HangHoaService.adjust_stock(
                ma_hang=hang_hoa.ma_hang,
                so_luong=-so_luong
            )

            thanhtien = so_luong * don_gia
            tongtien += thanhtien

            ChiTietHoaDonRepository.create(
                ma_hd=hoa_don.ma_hd,
                ma_hang=hang_hoa.ma_hang,
                so_luong=so_luong,
                don_gia=don_gia
            )

        # 4️⃣ Cập nhật tổng tiền
        HoaDonRepository.update(hoa_don.ma_hd, **{"tong_tien":Decimal(tongtien)})

        return HoaDonRepository.get_by_id(hoa_don.ma_hd)


    @staticmethod
    def get_all_hoa_don() -> QuerySet[HoaDon]:
        """
        Trả về QuerySet, giữ lazy loading để paginate/filter.
        """

        return HoaDonRepository.get_all()

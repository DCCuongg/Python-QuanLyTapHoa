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

        # Kiểm tra tồn kho trước
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

        tongtien = 0

        # Tạo chi tiết + trừ kho
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

        # Cập nhật tổng tiền
        HoaDonRepository.update(hoa_don.ma_hd, **{"tong_tien":Decimal(tongtien)})

        return HoaDonRepository.get_by_id(hoa_don.ma_hd)


    @staticmethod
    def get_all_hoa_don() -> QuerySet[HoaDon]:
        """
        Trả về QuerySet, giữ lazy loading để paginate/filter.
        """

        return HoaDonRepository.get_all()

    @staticmethod
    def get_hoa_don_by_nhan_vien(ma_nv: int) -> QuerySet[HoaDon]:
        """
        Lấy danh sách hóa đơn theo mã nhân viên.
        Trả về QuerySet để dễ paginate / filter ở View.
        """
        return HoaDonRepository.get_by_nhan_vien(ma_nv)

    @staticmethod
    def doanh_thu_theo_thang(nam: int):
        raw_data = HoaDonRepository.thong_ke_doanh_thu_theo_nam(nam)

        # map tháng → doanh thu
        doanh_thu_map = {
            item["thang"]: item["tong_doanh_thu"]
            for item in raw_data
        }

        # đảm bảo đủ 12 tháng
        result = []
        for thang in range(1, 13):
            result.append({
                "thang": thang,
                "tong_doanh_thu": doanh_thu_map.get(thang, Decimal(0))
            })

        return result

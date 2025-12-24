from typing import Optional
from django.db.models import QuerySet
from QuanLyHangHoa.models.hang_hoa import HangHoaRepository, HangHoa


class HangHoaService:

    @staticmethod
    def get_all() -> QuerySet[HangHoa]:
        """
        Trả về QuerySet để giữ lazy loading.
        View / DRF tự paginate, filter, serialize.
        """
        return HangHoaRepository.get_all()

    @staticmethod
    def get_by_id(ma_hang: int) -> Optional[HangHoa]:
        return HangHoaRepository.get_by_id(ma_hang)

    @staticmethod
    @staticmethod
    def create(**validated_data) -> HangHoa:
        """
        validated_data:
        {
            'ten_hang': str,
            'ma_dvt': DonViTinh instance,
            'ma_loai_hang': LoaiHang instance,
            'ma_thuong_hieu': ThuongHieu instance | None,
            'gia_nhap': float,
            'gia_ban': float,
            'so_luong_ton': int
        }
        """

        return HangHoaRepository.create(
            ten_hang=validated_data.get("ten_hang"),

            ma_dvt=validated_data["ma_dvt"].ma_dvt,
            ma_loai_hang=validated_data["ma_loai_hang"].ma_loai,

            ma_thuong_hieu=(
                validated_data["ma_thuong_hieu"].ma_thuong_hieu
                if validated_data.get("ma_thuong_hieu") else None
            ),

            gia_nhap=validated_data.get("gia_nhap", 0),
            gia_ban=validated_data.get("gia_ban", 0),
            so_luong_ton=validated_data.get("so_luong_ton", 0),
        )

    @staticmethod
    def update(ma_hang: int, **validated_data) -> Optional[HangHoa]:
        """
        Không validate lại dữ liệu.
        Tin tưởng Serializer.
        """
        return HangHoaRepository.update(ma_hang, **validated_data)

    @staticmethod
    def delete(ma_hang: int) -> bool:
        return HangHoaRepository.delete(ma_hang)

    @staticmethod
    def adjust_stock(ma_hang: int, so_luong: int) -> Optional[HangHoa]:
        """
        Đây là NGHIỆP VỤ → Service xử lý.
        Serializer không nên biết logic tồn kho.
        """
        obj = HangHoaRepository.get_by_id(ma_hang)
        if not obj:
            return None

        # nghiệp vụ: không cho âm tồn kho
        if obj.so_luong_ton + so_luong < 0:
            raise ValueError("Không đủ tồn kho")

        return HangHoaRepository.adjust_stock(ma_hang, so_luong)

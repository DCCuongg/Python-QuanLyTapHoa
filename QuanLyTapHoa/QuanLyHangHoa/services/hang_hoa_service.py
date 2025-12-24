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
    def create(**validated_data) -> HangHoa:
        """
        validated_data đã được Serializer validate.
        Service chỉ điều phối tạo dữ liệu.
        """
        return HangHoaRepository.create(**validated_data)

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

from typing import Optional
from django.db.models import QuerySet
from QuanLyHangHoa.models.hang_hoa import HangHoaRepository, HangHoa


class HangHoaService:
    """
    Lớp Service xử lý các nghiệp vụ liên quan đến hàng hóa.
    Đóng vai trò trung gian giữa tầng API/Serializer và Repository,
    đảm bảo logic nghiệp vụ không nằm ở View hay Serializer.
    """

    @staticmethod
    def get_all() -> QuerySet[HangHoa]:
        """
        Lấy danh sách tất cả hàng hóa.

        Trả về QuerySet để giữ cơ chế lazy loading,
        cho phép View hoặc DRF tự xử lý paginate, filter và serialize.

        Returns:
            QuerySet[HangHoa]: Danh sách hàng hóa.
        """
        return HangHoaRepository.get_all()

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
        return HangHoaRepository.get_by_id(ma_hang)

    @staticmethod
    @staticmethod
    def create(**validated_data) -> HangHoa:
        """
        Tạo mới hàng hóa từ dữ liệu đã được Serializer validate.

        validated_data có cấu trúc:
        {
            'ten_hang': str,
            'ma_dvt': DonViTinh instance,
            'ma_loai_hang': LoaiHang instance,
            'ma_thuong_hieu': ThuongHieu instance | None,
            'gia_nhap': float,
            'gia_ban': float,
            'so_luong_ton': int
        }

        Service chịu trách nhiệm chuyển đổi instance
        sang khóa ngoại (ID) để truyền cho Repository.

        Returns:
            HangHoa: Đối tượng hàng hóa vừa được tạo.
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
        Cập nhật thông tin hàng hóa.

        Không thực hiện validate lại dữ liệu,
        vì dữ liệu đã được Serializer kiểm tra hợp lệ.

        Args:
            ma_hang (int): Mã định danh của hàng hóa cần cập nhật.
            **validated_data: Các trường cần cập nhật và giá trị tương ứng.

        Returns:
            HangHoa | None: Đối tượng hàng hóa sau khi cập nhật,
            hoặc None nếu không tồn tại.
        """
        return HangHoaRepository.update(ma_hang, **validated_data)

    @staticmethod
    def delete(ma_hang: int) -> bool:
        """
        Xóa hàng hóa theo mã hàng.

        Args:
            ma_hang (int): Mã định danh của hàng hóa cần xóa.

        Returns:
            bool: True nếu xóa thành công, False nếu không tồn tại.
        """
        return HangHoaRepository.delete(ma_hang)

    @staticmethod
    def adjust_stock(ma_hang: int, so_luong: int) -> Optional[HangHoa]:
        """
        Điều chỉnh số lượng tồn kho của hàng hóa (cộng hoặc trừ).

        Đây là logic nghiệp vụ nên được xử lý tại Service,
        Serializer và View không cần biết chi tiết tồn kho.

        Ràng buộc nghiệp vụ:
        - Không cho phép tồn kho âm.

        Args:
            ma_hang (int): Mã định danh của hàng hóa.
            so_luong (int): Số lượng điều chỉnh (dương hoặc âm).

        Returns:
            HangHoa | None: Đối tượng hàng hóa sau khi cập nhật tồn kho,
            hoặc None nếu không tồn tại.

        Raises:
            ValueError: Khi số lượng tồn kho sau điều chỉnh nhỏ hơn 0.
        """
        obj = HangHoaRepository.get_by_id(ma_hang)
        if not obj:
            return None

        # nghiệp vụ: không cho âm tồn kho
        if obj.so_luong_ton + so_luong < 0:
            raise ValueError("Không đủ tồn kho")

        return HangHoaRepository.adjust_stock(ma_hang, so_luong)

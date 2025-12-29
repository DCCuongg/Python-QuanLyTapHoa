"""
Serializers cho module Hóa Đơn.

- ChiTietHoaDonSerializer:
    + READ: trả về thông tin hàng hóa dạng object
    + WRITE: nhận ID hàng hóa để tạo chi tiết hóa đơn

- HoaDonSerializer:
    + Nhận danh sách chi tiết hóa đơn
    + Validate số lượng và nghiệp vụ cơ bản
"""

from rest_framework import serializers
from QuanLyHangHoa.models.hang_hoa import HangHoa
from QuanLyHoaDon.models.chi_tiet_hoa_don import ChiTietHoaDon
from QuanLyHangHoa.serializers import HangHoaSerializer
from QuanLyHoaDon.models.hoa_don import HoaDon


class ChiTietHoaDonSerializer(serializers.ModelSerializer):
    """
    Serializer cho ChiTietHoaDon.

    READ:
        - Trả về thông tin hàng hóa (object lồng).
    WRITE:
        - Nhận hang_hoa_id để tạo chi tiết hóa đơn.
    """

    # READ
    hang_hoa = HangHoaSerializer(read_only=True)

    # WRITE
    hang_hoa_id = serializers.PrimaryKeyRelatedField(
        queryset=HangHoa.objects.all(),
        source="hang_hoa",
        write_only=True
    )

    class Meta:
        model = ChiTietHoaDon
        fields = [
            "hang_hoa",
            "hang_hoa_id",
            "so_luong",
            "don_gia",
            "thanh_tien",
        ]
        read_only_fields = ["thanh_tien", "don_gia"]

    def validate_so_luong(self, value):
        """
        Validate số lượng sản phẩm phải > 0.
        """
        if value <= 0:
            raise serializers.ValidationError("Số lượng phải > 0")
        return value


class HoaDonSerializer(serializers.ModelSerializer):
    """
    Serializer cho HoaDon.

    - Nhận danh sách chi tiết hóa đơn.
    - Tổng tiền và ngày lập được tính ở Service.
    """

    chi_tiets = ChiTietHoaDonSerializer(many=True, required=True)

    class Meta:
        model = HoaDon
        fields = [
            "ma_hd",
            "ngay_lap",
            "nhan_vien",
            "tong_tien",
            "chi_tiets",
        ]
        read_only_fields = ["ma_hd", "tong_tien", "ngay_lap"]

    def create(self, validated_data):
        """
        Tạo hóa đơn và các chi tiết hóa đơn tương ứng.
        (Logic chính vẫn xử lý ở Service)
        """
        chi_tiets_data = validated_data.pop("chi_tiets")
        hoa_don = HoaDon.objects.create(**validated_data)

        for item in chi_tiets_data:
            ChiTietHoaDon.objects.create(
                hoa_don=hoa_don,
                **item
            )

        return hoa_don

    def validate_chi_tiets(self, value):
        """
        Hóa đơn phải có ít nhất 1 sản phẩm hợp lệ (số lượng > 0).
        """
        valid_items = [
            item for item in value
            if item.get("so_luong", 0) > 0
        ]

        if not valid_items:
            raise serializers.ValidationError(
                "Hóa đơn phải có ít nhất 1 sản phẩm hợp lệ (số lượng > 0)"
            )

        return valid_items

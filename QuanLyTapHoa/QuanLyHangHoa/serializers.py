from rest_framework import serializers

from QuanLyHangHoa.models.don_vi_tinh import DonViTinh
from QuanLyHangHoa.models.loai_hang import LoaiHang
from QuanLyHangHoa.models.thuong_hieu import ThuongHieu
from QuanLyHangHoa.models.hang_hoa import HangHoa


# =========================
# DonViTinh Serializer
# =========================
class DonViTinhSerializer(serializers.ModelSerializer):
    """
    Serializer dùng để chuyển đổi dữ liệu Đơn Vị Tính
    giữa Model và JSON trong API.
    """

    class Meta:
        model = DonViTinh
        fields = ["ma_dvt", "ten_dvt"]


# =========================
# LoaiHang Serializer
# =========================
class LoaiHangSerializer(serializers.ModelSerializer):
    """
    Serializer dùng để chuyển đổi dữ liệu Loại Hàng
    giữa Model và JSON trong API.
    """

    class Meta:
        model = LoaiHang
        fields = ["ma_loai", "ten_loai", "mo_ta"]


# =========================
# ThuongHieu Serializer
# =========================
class ThuongHieuSerializer(serializers.ModelSerializer):
    """
    Serializer dùng để chuyển đổi dữ liệu Thương Hiệu
    giữa Model và JSON trong API.
    """

    class Meta:
        model = ThuongHieu
        fields = ["ma_thuong_hieu", "ten_thuong_hieu", "quoc_gia", "mo_ta"]


# =========================
# HangHoa Serializer (LỒNG OBJECT)
# =========================
class HangHoaSerializer(serializers.ModelSerializer):
    """
    Serializer dùng cho Hàng Hóa.

    - READ: Trả về thông tin hàng hóa kèm object lồng
      (đơn vị tính, loại hàng, thương hiệu).
    - WRITE: Nhận khóa ngoại dưới dạng ID.
    """

    # =====================
    # READ: object lồng
    # =====================
    don_vi_tinh = DonViTinhSerializer(
        source="ma_dvt",
        read_only=True
    )

    loai_hang = LoaiHangSerializer(
        source="ma_loai_hang",
        read_only=True
    )

    thuong_hieu = ThuongHieuSerializer(
        source="ma_thuong_hieu",
        read_only=True
    )

    # =====================
    # WRITE: nhận ID
    # =====================
    ma_dvt = serializers.PrimaryKeyRelatedField(
        queryset=DonViTinh.objects.all(),
        write_only=True
    )

    ma_loai_hang = serializers.PrimaryKeyRelatedField(
        queryset=LoaiHang.objects.all(),
        write_only=True
    )

    ma_thuong_hieu = serializers.PrimaryKeyRelatedField(
        queryset=ThuongHieu.objects.all(),
        write_only=True,
        allow_null=True,
        required=False
    )

    class Meta:
        model = HangHoa
        fields = [
            "ma_hang",
            "ten_hang",

            # READ
            "don_vi_tinh",
            "loai_hang",
            "thuong_hieu",

            # WRITE
            "ma_dvt",
            "ma_loai_hang",
            "ma_thuong_hieu",

            "gia_nhap",
            "gia_ban",
            "so_luong_ton",
        ]

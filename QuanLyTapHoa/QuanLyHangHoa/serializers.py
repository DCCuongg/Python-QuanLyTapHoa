from rest_framework import serializers

from QuanLyHangHoa.models.don_vi_tinh import DonViTinh
from QuanLyHangHoa.models.loai_hang import LoaiHang
from QuanLyHangHoa.models.thuong_hieu import ThuongHieu
from QuanLyHangHoa.models.hang_hoa import HangHoa


# =========================
# DonViTinh Serializer
# =========================
class DonViTinhSerializer(serializers.ModelSerializer):
    class Meta:
        model = DonViTinh
        fields = ["ma_dvt", "ten_dvt"]


# =========================
# LoaiHang Serializer
# =========================
class LoaiHangSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoaiHang
        fields = ["ma_loai", "ten_loai", "mo_ta"]


# =========================
# ThuongHieu Serializer
# =========================
class ThuongHieuSerializer(serializers.ModelSerializer):
    class Meta:
        model = ThuongHieu
        fields = ["ma_thuong_hieu", "ten_thuong_hieu", "quoc_gia", "mo_ta"]


# =========================
# HangHoa Serializer (LỒNG OBJECT)
# =========================
class HangHoaSerializer(serializers.ModelSerializer):
    # READ: trả object lồng
    ma_dvt = DonViTinhSerializer(read_only=True)
    ma_loai_hang = LoaiHangSerializer(read_only=True)
    ma_thuong_hieu = ThuongHieuSerializer(read_only=True)

    # WRITE: nhận ID
    ma_dvt_id = serializers.PrimaryKeyRelatedField(
        queryset=DonViTinh.objects.all(),
        source="ma_dvt",
        write_only=True
    )

    ma_loai_hang_id = serializers.PrimaryKeyRelatedField(
        queryset=LoaiHang.objects.all(),
        source="ma_loai_hang",
        write_only=True
    )

    ma_thuong_hieu_id = serializers.PrimaryKeyRelatedField(
        queryset=ThuongHieu.objects.all(),
        source="ma_thuong_hieu",
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
            "ma_dvt",
            "ma_loai_hang",
            "ma_thuong_hieu",

            # WRITE
            "ma_dvt_id",
            "ma_loai_hang_id",
            "ma_thuong_hieu_id",

            "gia_nhap",
            "gia_ban",
            "so_luong_ton",
        ]

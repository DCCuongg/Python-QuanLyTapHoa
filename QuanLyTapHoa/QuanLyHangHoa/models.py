from django.db import models

# Create your models here.

# =========================
# Models cho bảng LOAIHANG
# =========================
class LoaiHang(models.Model):
    ma_loai = models.AutoField(primary_key=True, db_column="MaLoaiHang")
    ten_loai = models.CharField(max_length=100, db_column="TenLoaiHang")
    mo_ta = models.CharField(max_length=255, null=True, blank=True, db_column="MoTa")

    class Meta:
        db_table = "LOAI_HANG"

    def __str__(self):
        return self.ten_loai


# =========================
# Models cho bảng THUONGHIEU
# =========================
class ThuongHieu(models.Model):
    ma_thuong_hieu = models.AutoField(primary_key=True)  # tương đương INT IDENTITY(1,1)
    ten_thuong_hieu = models.CharField(max_length=100, null=False)
    quoc_gia = models.CharField(max_length=100, null=True, blank=True)
    mo_ta = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        db_table = 'THUONG_HIEU'  # giữ tên bảng giống SQL Server

    def __str__(self):
        return self.ten_thuong_hieu


# =========================
# Models cho bảng DONVITINH
# =========================
class DonViTinh(models.Model):
    ma_dvt = models.AutoField(primary_key=True)  # tương đương INT IDENTITY(1,1)
    ten_dvt = models.CharField(max_length=50, null=False)

    class Meta:
        db_table = 'DON_VI_TINH'  # giữ tên bảng giống SQL Server

    def __str__(self):
        return self.ten_dvt


# =========================
# Models cho bảng HANGHOA
# =========================
class HangHoa(models.Model):
    ma_hang = models.AutoField(primary_key=True)
    ten_hang = models.CharField(max_length=150, null=False)

    ma_thuong_hieu = models.ForeignKey(
        'ThuongHieu',  # model đã tạo trước
        on_delete=models.SET_NULL,  # khi thương hiệu bị xóa, giữ sản phẩm với giá trị NULL
        null=True,
        blank=True,
        db_column='MaThuongHieu',
        related_name='hang_hoas'
    )

    ma_loai_hang = models.ForeignKey(
        'LoaiHang',  # giả sử bạn đã có model LoaiHang
        on_delete=models.PROTECT,  # không cho xóa loại hàng nếu còn hàng tồn
        db_column='MaLoaiHang',
        related_name='hang_hoas'
    )

    ma_dvt = models.ForeignKey(
        'DonViTinh',
        on_delete=models.PROTECT,
        db_column='MaDVT',
        related_name='hang_hoas'
    )

    gia_nhap = models.DecimalField(max_digits=18, decimal_places=2)
    gia_ban = models.DecimalField(max_digits=18, decimal_places=2)
    so_luong_ton = models.IntegerField()

    class Meta:
        db_table = 'HANG_HOA'

    def __str__(self):
        return self.ten_hang
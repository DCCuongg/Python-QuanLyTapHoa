from typing import Optional, List
from decimal import Decimal

from QuanLyNhanSu.models.chuc_vu import ChucVuRepository, ChucVu
from QuanLyNhanSu.models.nhan_vien import NhanVienRepository, NhanVien
from QuanLyHoaDon.models.hoa_don import HoaDonRepository
from QuanLyNhanSu.models.tham_so import ThamSoLuongRepository


# =========================
# ChucVuService
# =========================
class ChucVuService:
    """
    Service xử lý nghiệp vụ liên quan đến Chức vụ.

    Chịu trách nhiệm:
    - Điều phối thao tác CRUD cho Chức vụ
    - Kiểm tra ràng buộc nghiệp vụ (ví dụ: không cho xóa chức vụ đang được nhân viên sử dụng)
    """

    @staticmethod
    def list_all() -> List[ChucVu]:
        """
        Lấy danh sách tất cả chức vụ.

        Returns:
            List[ChucVu]: Danh sách chức vụ
        """
        return ChucVuRepository.get_all()

    @staticmethod
    def get(ma_chuc_vu: int) -> Optional[ChucVu]:
        """
        Lấy thông tin chức vụ theo mã.

        Args:
            ma_chuc_vu (int): Mã chức vụ

        Returns:
            ChucVu | None
        """
        return ChucVuRepository.get_by_id(ma_chuc_vu)

    @staticmethod
    def create(
        ten_chuc_vu: str,
        phu_cap=0,
        he_so_luong=1,
        ghi_chu: str = None
    ) -> ChucVu:
        """
        Tạo mới chức vụ.

        Returns:
            ChucVu: Đối tượng chức vụ vừa tạo
        """
        return ChucVuRepository.create(
            ten_chuc_vu,
            phu_cap,
            he_so_luong,
            ghi_chu
        )

    @staticmethod
    def update(ma_chuc_vu: int, **kwargs) -> Optional[ChucVu]:
        """
        Cập nhật thông tin chức vụ.

        Returns:
            ChucVu | None
        """
        return ChucVuRepository.update(ma_chuc_vu, **kwargs)

    @staticmethod
    def delete(ma_chuc_vu: int) -> bool:
        """
        Xóa chức vụ.

        Không cho phép xóa nếu chức vụ đang được nhân viên sử dụng.

        Returns:
            bool: True nếu xóa thành công, False nếu không xóa được
        """
        cv = ChucVuRepository.get_by_id(ma_chuc_vu)
        if cv and cv.nhan_viens.exists():
            return False
        return ChucVuRepository.delete(ma_chuc_vu)


# =========================
# NhanVienService
# =========================
class NhanVienService:
    """
    Service xử lý nghiệp vụ liên quan đến Nhân viên.

    Bao gồm:
    - CRUD nhân viên
    - Tìm kiếm, lọc
    - Thống kê bán hàng
    - Tính lương
    """

    @staticmethod
    def list_all() -> List[NhanVien]:
        """
        Lấy danh sách tất cả nhân viên.
        """
        return NhanVienRepository.get_all()

    @staticmethod
    def get(ma_nv: int) -> Optional[NhanVien]:
        """
        Lấy thông tin nhân viên theo mã.
        """
        return NhanVienRepository.get_by_id(ma_nv)

    @staticmethod
    def create(
        ho_ten: str,
        ma_chuc_vu: int,
        sdt: str = None,
        dia_chi: str = None
    ) -> NhanVien:
        """
        Tạo mới nhân viên.

        Raises:
            ValueError: Nếu chức vụ không tồn tại
        """
        if not ChucVuRepository.get_by_id(ma_chuc_vu):
            raise ValueError("Chức vụ không tồn tại")
        return NhanVienRepository.create(
            ho_ten,
            ma_chuc_vu,
            sdt,
            dia_chi
        )

    @staticmethod
    def update(ma_nv: int, **kwargs) -> Optional[NhanVien]:
        """
        Cập nhật thông tin nhân viên.

        Raises:
            ValueError: Nếu cập nhật chức vụ không tồn tại
        """
        if 'ma_chuc_vu' in kwargs:
            if not ChucVuRepository.get_by_id(kwargs['ma_chuc_vu']):
                raise ValueError("Chức vụ không tồn tại")
        return NhanVienRepository.update(ma_nv, **kwargs)

    @staticmethod
    def delete(ma_nv: int) -> bool:
        """
        Xóa nhân viên theo mã.
        """
        return NhanVienRepository.delete(ma_nv)

    @staticmethod
    def search(keyword: str):
        """
        Tìm kiếm nhân viên theo tên (không phân biệt hoa thường).
        """
        if not keyword or not keyword.strip():
            return NhanVien.objects.none()

        return NhanVien.objects.filter(
            ho_ten__icontains=keyword.strip()
        )

    @staticmethod
    def filter_by_chuc_vu(ma_chuc_vu: int) -> List[NhanVien]:
        """
        Lọc danh sách nhân viên theo chức vụ.
        """
        return (
            NhanVien.objects
            .filter(ma_chuc_vu_id=ma_chuc_vu)
            .select_related('ma_chuc_vu')
        )

    @staticmethod
    def thong_ke_ban_hang():
        """
        Thống kê số hóa đơn và tổng doanh thu của mỗi nhân viên.

        Returns:
            List[dict]: Danh sách thống kê
        """
        raw_data = HoaDonRepository.thong_ke_theo_nhan_vien()

        result = []
        for item in raw_data:
            result.append({
                "ma_nv": item["nhan_vien_id"],
                "ho_ten": item["nhan_vien__ho_ten"],
                "so_hoa_don": item["so_hoa_don"],
                "tong_doanh_thu": item["tong_doanh_thu"] or Decimal(0)
            })
        return result

    @staticmethod
    def tinh_luong_nhan_vien(ma_nv: int) -> Decimal:
        """
        Tính lương cho một nhân viên.

        Công thức:
        lương = lương cơ bản * hệ số + phụ cấp
        """
        nv = NhanVienRepository.get_by_id(ma_nv)
        if not nv:
            raise ValueError("Nhân viên không tồn tại")

        tham_so = ThamSoLuongRepository.get_luong_co_ban_hien_tai()
        if not tham_so or not tham_so.gia_tri_so:
            raise ValueError("Chưa cấu hình lương cơ bản")

        luong_co_ban = Decimal(tham_so.gia_tri_so)
        chuc_vu = nv.ma_chuc_vu

        return (
            luong_co_ban * Decimal(chuc_vu.he_so_luong)
            + Decimal(chuc_vu.phu_cap or 0)
        )

    @staticmethod
    def tinh_luong_tat_ca():
        """
        Tính lương cho toàn bộ nhân viên.

        Returns:
            List[dict]: Danh sách lương từng nhân viên
        """
        tham_so = ThamSoLuongRepository.get_luong_co_ban_hien_tai()
        luong_co_ban = Decimal(tham_so.gia_tri_so)

        nhan_viens = NhanVien.objects.select_related('ma_chuc_vu')

        result = []
        for nv in nhan_viens:
            luong = (
                luong_co_ban * Decimal(nv.ma_chuc_vu.he_so_luong)
                + Decimal(nv.ma_chuc_vu.phu_cap or 0)
            )
            result.append({
                "ma_nv": nv.ma_nv,
                "ho_ten": nv.ho_ten,
                "chuc_vu": nv.ma_chuc_vu.ten_chuc_vu,
                "luong": luong
            })

        return result

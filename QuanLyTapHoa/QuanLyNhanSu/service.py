from typing import Optional, List
from QuanLyNhanSu.models.chuc_vu import ChucVuRepository,ChucVu  
from QuanLyNhanSu.models.nhan_vien import NhanVienRepository, NhanVien
from decimal import Decimal
from QuanLyHoaDon.models.hoa_don import HoaDonRepository
from QuanLyNhanSu.models.tham_so import ThamSoLuongRepository
from QuanLyNhanSu.models.nhan_vien import NhanVienRepository
# ChucVuService
class ChucVuService:

    @staticmethod
    def list_all() -> List[ChucVu]:
        return ChucVuRepository.get_all()

    @staticmethod
    def get(ma_chuc_vu: int) -> Optional[ChucVu]:
        return ChucVuRepository.get_by_id(ma_chuc_vu)

    @staticmethod
    def create(ten_chuc_vu: str, phu_cap=0, he_so_luong=1, ghi_chu: str = None) -> ChucVu:
        return ChucVuRepository.create(ten_chuc_vu, phu_cap, he_so_luong, ghi_chu)

    @staticmethod
    def update(ma_chuc_vu: int, **kwargs) -> Optional[ChucVu]:
        return ChucVuRepository.update(ma_chuc_vu, **kwargs)

    @staticmethod
    def delete(ma_chuc_vu: int) -> bool:
        #kiểm tra xem có nhân viên đang dùng chức vụ không
        cv = ChucVuRepository.get_by_id(ma_chuc_vu)
        if cv and cv.nhan_viens.exists():
            return False  # không xóa được
        return ChucVuRepository.delete(ma_chuc_vu)


# NhanVienService
class NhanVienService:

    @staticmethod
    def list_all() -> List[NhanVien]:
        return NhanVienRepository.get_all()

    @staticmethod
    def get(ma_nv: int) -> Optional[NhanVien]:
        return NhanVienRepository.get_by_id(ma_nv)

    @staticmethod
    def create(ho_ten: str, ma_chuc_vu: int, sdt: str = None, dia_chi: str = None) -> NhanVien:
        # kiểm tra chức vụ tồn tại
        if not ChucVuRepository.get_by_id(ma_chuc_vu):
            raise ValueError("Chức vụ không tồn tại")
        return NhanVienRepository.create(ho_ten, ma_chuc_vu, sdt, dia_chi)

    @staticmethod
    def update(ma_nv: int, **kwargs) -> Optional[NhanVien]:
        # Nếu cập nhật chức vụ, kiểm tra tồn tại
        if 'ma_chuc_vu' in kwargs:
            if not ChucVuRepository.get_by_id(kwargs['ma_chuc_vu']):
                raise ValueError("Chức vụ không tồn tại")
        return NhanVienRepository.update(ma_nv, **kwargs)

    @staticmethod
    def delete(ma_nv: int) -> bool:
        return NhanVienRepository.delete(ma_nv)

    #tìm theo tên
    @staticmethod
    def search(keyword: str):
        if not keyword or not keyword.strip():
            return NhanVien.objects.none() 

        return NhanVien.objects.filter(
        ho_ten__icontains=keyword.strip()
    )

    #tìm theo chức vụ
    @staticmethod
    def filter_by_chuc_vu(ma_chuc_vu: int) -> List[NhanVien]:
        return NhanVien.objects.filter(ma_chuc_vu_id=ma_chuc_vu).select_related('ma_chuc_vu')

    @staticmethod

    def thong_ke_ban_hang():
        """
        Thống kê số hóa đơn và tổng doanh thu của mỗi nhân viên
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
        # 1. Lấy nhân viên
        nv = NhanVienRepository.get_by_id(ma_nv)
        if not nv:
            raise ValueError("Nhân viên không tồn tại")

        # 2. Lấy lương cơ bản
        tham_so = ThamSoLuongRepository.get_luong_co_ban_hien_tai()
        if not tham_so or not tham_so.gia_tri_so:
            raise ValueError("Chưa cấu hình lương cơ bản")

        luong_co_ban = Decimal(tham_so.gia_tri_so)

        # 3. Lấy chức vụ
        chuc_vu = nv.ma_chuc_vu
        he_so = Decimal(chuc_vu.he_so_luong)
        phu_cap = Decimal(chuc_vu.phu_cap or 0)

        # 4. Tính lương
        luong = luong_co_ban * he_so + phu_cap

        return luong

    @staticmethod
    def tinh_luong_tat_ca():
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
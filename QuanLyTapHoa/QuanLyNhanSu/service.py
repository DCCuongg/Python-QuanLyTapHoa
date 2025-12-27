from typing import Optional, List
from QuanLyNhanSu.models.chuc_vu import ChucVuRepository,ChucVu  
from QuanLyNhanSu.models.nhan_vien import NhanVienRepository, NhanVien

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
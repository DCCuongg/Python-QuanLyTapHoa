

from QuanLyHangHoa.models.hang_hoa import HangHoaRepository

class HangHoaService:
    @staticmethod
    def get_all():
        return HangHoaRepository.get_all()
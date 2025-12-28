# views/hoa_don_views.py
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from QuanLyHoaDon.serializers import HoaDonSerializer
from QuanLyHoaDon.services.hoa_don_service import HoaDonService


@api_view(['POST'])
def hoa_don_create(request):
    """
    API tạo hóa đơn.
    Input JSON:
    {
        "nhan_vien": 1,
        "chi_tiet_hoa_dons": [
            {"hang_hoa_id": 101, "so_luong": 2},
            {"hang_hoa_id": 102, "so_luong": 5}
        ]
    }
    """
    serializer = HoaDonSerializer(data=request.data)
    if serializer.is_valid():
        try:
            hoa_don = HoaDonService.create_hoa_don(serializer.validated_data)
            result = HoaDonSerializer(hoa_don).data  # serialize trả về
            return Response(result, status=status.HTTP_201_CREATED)
        except ValueError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def hoa_don_get_all(request):
    """
    Lấy tất cả hóa đơn.
    Trả về JSON với danh sách chi tiết hóa đơn.
    """
    qs = HoaDonService.get_all_hoa_don()  # trả về QuerySet → vẫn lazy loading
    serializer = HoaDonSerializer(qs, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def hoa_don_get_by_nhan_vien(request, ma_nv: int):
    """
    Lấy danh sách hóa đơn theo mã nhân viên.

    URL ví dụ:
    GET /api/hoa-don/nhan-vien/1/
    """
    qs = HoaDonService.get_hoa_don_by_nhan_vien(ma_nv)

    if not qs.exists():
        return Response(
            {"detail": "Nhân viên chưa có hóa đơn nào"},
            status=status.HTTP_404_NOT_FOUND
        )

    serializer = HoaDonSerializer(qs, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def doanh_thu_theo_thang(request):
    nam = request.query_params.get('nam')

    if not nam:
        return Response(
            {"error": "Thiếu tham số năm"},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        nam = int(nam)
    except ValueError:
        return Response(
            {"error": "Năm không hợp lệ"},
            status=status.HTTP_400_BAD_REQUEST
        )

    data = HoaDonService.doanh_thu_theo_thang(nam)
    return Response(data)
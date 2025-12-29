"""
Module chứa các API xử lý nghiệp vụ Hóa Đơn.

Bao gồm:
- Tạo hóa đơn
- Lấy danh sách hóa đơn
- Lấy hóa đơn theo nhân viên
- Thống kê doanh thu theo tháng
"""

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from QuanLyHoaDon.serializers import HoaDonSerializer
from QuanLyHoaDon.services.hoa_don_service import HoaDonService


@api_view(['POST'])
def hoa_don_create(request):
    """
    Tạo mới một hóa đơn bán hàng.

    Request body (JSON):
    {
        "nhan_vien": 1,
        "chi_tiets": [
            {"hang_hoa_id": 101, "so_luong": 2},
            {"hang_hoa_id": 102, "so_luong": 5}
        ]
    }

    Quy trình:
    - Validate dữ liệu bằng serializer
    - Kiểm tra tồn kho
    - Tạo hóa đơn + chi tiết hóa đơn
    - Trừ tồn kho tương ứng

    Response:
    - 201: Tạo thành công
    - 400: Lỗi dữ liệu hoặc tồn kho không đủ
    """
    serializer = HoaDonSerializer(data=request.data)
    if serializer.is_valid():
        try:
            hoa_don = HoaDonService.create_hoa_don(serializer.validated_data)
            return Response(
                HoaDonSerializer(hoa_don).data,
                status=status.HTTP_201_CREATED
            )
        except ValueError as e:
            return Response(
                {"detail": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def hoa_don_get_all(request):
    """
    Lấy danh sách toàn bộ hóa đơn.

    Response:
    - Danh sách hóa đơn kèm chi tiết.
    """
    qs = HoaDonService.get_all_hoa_don()
    serializer = HoaDonSerializer(qs, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def hoa_don_get_by_nhan_vien(request, ma_nv: int):
    """
    Lấy danh sách hóa đơn theo mã nhân viên.

    URL:
    GET /api/hoa-don/nhan-vien/<ma_nv>/

    Response:
    - 200: Danh sách hóa đơn
    - 404: Nhân viên chưa có hóa đơn
    """
    qs = HoaDonService.get_hoa_don_by_nhan_vien(ma_nv)

    if not qs.exists():
        return Response(
            {"detail": "Nhân viên chưa có hóa đơn nào"},
            status=status.HTTP_404_NOT_FOUND
        )

    serializer = HoaDonSerializer(qs, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def doanh_thu_theo_thang(request):
    """
    Thống kê doanh thu theo từng tháng trong năm.

    Query params:
    ?nam=2025

    Response:
    [
        {"thang": 1, "tong_doanh_thu": 1000000},
        ...
        {"thang": 12, "tong_doanh_thu": 0}
    ]
    """
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

"""
Views cho module Quản Lý Hàng Hóa.

File này định nghĩa các API endpoint liên quan đến nghiệp vụ hàng hóa,
tuân theo kiến trúc phân tầng:
- View: tiếp nhận request, validate dữ liệu đầu vào, trả response
- Service: xử lý nghiệp vụ
- Repository/Model: thao tác cơ sở dữ liệu

Các API hỗ trợ:
- Lấy danh sách hàng hóa
- Lấy chi tiết hàng hóa theo mã
- Tạo mới hàng hóa
- Cập nhật thông tin hàng hóa
- Xóa hàng hóa
- Điều chỉnh tồn kho
"""

from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response

from QuanLyHangHoa.services.hang_hoa_service import HangHoaService
from QuanLyHangHoa.serializers import HangHoaSerializer


@api_view(['GET'])
def hanghoa_get_all(request):
    """
    Lấy danh sách tất cả hàng hóa.

    Method: GET
    URL: /api/hanghoa/

    Response:
        200 OK: Danh sách hàng hóa
    """
    qs = HangHoaService.get_all()
    serializer = HangHoaSerializer(qs, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def hanghoa_get_by_id(request, ma_hang: int):
    """
    Lấy thông tin chi tiết của một hàng hóa theo mã.

    Method: GET
    URL: /api/hanghoa/<ma_hang>/

    Params:
        ma_hang (int): Mã hàng hóa

    Response:
        200 OK: Thông tin hàng hóa
        404 NOT FOUND: Hàng hóa không tồn tại
    """
    obj = HangHoaService.get_by_id(ma_hang)
    if not obj:
        return Response(
            {"error": "Hàng hóa không tồn tại"},
            status=404
        )

    serializer = HangHoaSerializer(obj)
    return Response(serializer.data)


@api_view(["POST"])
def hanghoa_create(request):
    """
    Tạo mới một hàng hóa.

    Method: POST
    URL: /api/hanghoa/

    Body:
        Dữ liệu hàng hóa hợp lệ theo HangHoaSerializer

    Response:
        201 CREATED: Hàng hóa được tạo thành công
        400 BAD REQUEST: Dữ liệu không hợp lệ
    """
    serializer = HangHoaSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    obj = HangHoaService.create(**serializer.validated_data)

    return Response(
        HangHoaSerializer(obj).data,
        status=201
    )


@api_view(['PUT'])
def hanghoa_update(request, ma_hang: int):
    """
    Cập nhật thông tin hàng hóa.

    Method: PUT
    URL: /api/hanghoa/<ma_hang>/

    Params:
        ma_hang (int): Mã hàng hóa

    Body:
        Các trường cần cập nhật (partial update)

    Response:
        200 OK: Cập nhật thành công
        404 NOT FOUND: Hàng hóa không tồn tại
    """
    serializer = HangHoaSerializer(data=request.data, partial=True)
    serializer.is_valid(raise_exception=True)

    obj = HangHoaService.update(ma_hang, **serializer.validated_data)
    if not obj:
        return Response(
            {"error": "Hàng hóa không tồn tại"},
            status=404
        )

    return Response(HangHoaSerializer(obj).data)


@api_view(['DELETE'])
def hanghoa_delete(request, ma_hang: int):
    """
    Xóa một hàng hóa theo mã.

    Method: DELETE
    URL: /api/hanghoa/<ma_hang>/

    Params:
        ma_hang (int): Mã hàng hóa

    Response:
        204 NO CONTENT: Xóa thành công
        404 NOT FOUND: Hàng hóa không tồn tại
    """
    success = HangHoaService.delete(ma_hang)
    if not success:
        return Response(
            {"error": "Hàng hóa không tồn tại"},
            status=404
        )

    return Response({"message": "Xóa hàng hóa thành công"},status=204)


@api_view(['POST'])
def hanghoa_adjust_stock(request, ma_hang: int):
    """
    Điều chỉnh số lượng tồn kho của hàng hóa.

    Method: POST
    URL: /api/hanghoa/<ma_hang>/adjust-stock/

    Params:
        ma_hang (int): Mã hàng hóa

    Body:
        so_luong (int): Số lượng thay đổi (có thể âm hoặc dương)

    Response:
        200 OK: Điều chỉnh tồn kho thành công
        400 BAD REQUEST: Thiếu dữ liệu hoặc tồn kho âm
        404 NOT FOUND: Hàng hóa không tồn tại
    """
    so_luong = request.data.get("so_luong")

    if so_luong is None:
        return Response(
            {"error": "Thiếu so_luong"},
            status=400
        )

    try:
        obj = HangHoaService.adjust_stock(ma_hang, int(so_luong))
        if not obj:
            return Response(
                {"error": "Hàng hóa không tồn tại"},
                status=404
            )

        return Response(HangHoaSerializer(obj).data)

    except ValueError as e:
        return Response(
            {"error": str(e)},
            status=400
        )

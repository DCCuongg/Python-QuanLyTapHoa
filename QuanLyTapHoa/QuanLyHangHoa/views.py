from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.response import Response

from QuanLyHangHoa.services.hang_hoa_service import HangHoaService
from QuanLyHangHoa.serializers import HangHoaSerializer

@api_view(['GET'])
def hanghoa_get_all(request):
    qs = HangHoaService.get_all()
    serializer = HangHoaSerializer(qs, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def hanghoa_get_by_id(request, ma_hang: int):
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
    serializer = HangHoaSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)  # sai là dừng ở đây

    obj = HangHoaService.create(**serializer.validated_data)  # dùng data gốc

    return Response(
        HangHoaSerializer(obj).data,
        status=201
    )

@api_view(['PUT'])
def hanghoa_update(request, ma_hang: int):
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
    success = HangHoaService.delete(ma_hang)
    if not success:
        return Response(
            {"error": "Hàng hóa không tồn tại"},
            status=404
        )

    return Response(
        {"message": "Xóa hàng hóa thành công"},
        status=204
    )

@api_view(['POST'])
def hanghoa_adjust_stock(request, ma_hang: int):
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
        # bắt nghiệp vụ: tồn kho âm
        return Response(
            {"error": str(e)},
            status=400
        )



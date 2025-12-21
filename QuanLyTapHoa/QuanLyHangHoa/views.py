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

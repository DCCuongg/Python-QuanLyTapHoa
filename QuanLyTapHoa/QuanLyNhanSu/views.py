from django.shortcuts import render
from rest_framework import status, viewsets
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from .serializer import ChucVuSerializer, NhanVienSerializer
from .service import ChucVuService, NhanVienService
from QuanLyNhanSu.models.chuc_vu import ChucVu
from QuanLyNhanSu.models.nhan_vien import NhanVien
# ==================== HÀM VIEW CHO URLS ====================

# ---------- Chức vụ ----------
@api_view(['GET'])
def chucvu_get_all(request):
    """GET: Lấy tất cả chức vụ"""
    queryset = ChucVuService.list_all()
    serializer = ChucVuSerializer(queryset, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def chucvu_get_by_id(request, ma_chuc_vu):
    """GET: Lấy chức vụ theo ID"""
    obj = ChucVuService.get(ma_chuc_vu)
    if not obj:
        return Response({"detail": "Chức vụ không tồn tại"}, status=status.HTTP_404_NOT_FOUND)
    serializer = ChucVuSerializer(obj)
    return Response(serializer.data)

@api_view(['POST'])
def chucvu_create(request):
    """POST: Tạo chức vụ mới"""
    data = request.data
    obj = ChucVuService.create(
        ten_chuc_vu=data.get('ten_chuc_vu'),
        phu_cap=data.get('phu_cap', 0),
        he_so_luong=data.get('he_so_luong', 1),
        ghi_chu=data.get('ghi_chu')
    )
    serializer = ChucVuSerializer(obj)
    return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['PUT'])
def chucvu_update(request, ma_chuc_vu):
    """PUT: Cập nhật chức vụ"""
    obj = ChucVuService.update(ma_chuc_vu, **request.data)
    if not obj:
        return Response({"detail": "Chức vụ không tồn tại"}, status=status.HTTP_404_NOT_FOUND)
    serializer = ChucVuSerializer(obj)
    return Response(serializer.data)

@api_view(['DELETE'])
def chucvu_delete(request, ma_chuc_vu):
    """DELETE: Xóa chức vụ"""
    success = ChucVuService.delete(ma_chuc_vu)
    if not success:
        return Response({"detail": "Không thể xóa chức vụ (có nhân viên đang sử dụng hoặc không tồn tại)"},
                        status=status.HTTP_400_BAD_REQUEST)
    return Response(status=status.HTTP_204_NO_CONTENT)


# ---------- Nhân viên ----------
@api_view(['GET'])
def nhanvien_get_all(request):
    """GET: Lấy tất cả nhân viên"""
    queryset = NhanVienService.list_all()
    serializer = NhanVienSerializer(queryset, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def nhanvien_get_by_id(request, ma_nv):
    """GET: Lấy nhân viên theo ID"""
    obj = NhanVienService.get(ma_nv)
    if not obj:
        return Response({"detail": "Nhân viên không tồn tại"}, status=status.HTTP_404_NOT_FOUND)
    serializer = NhanVienSerializer(obj)
    return Response(serializer.data)

@api_view(['POST'])
def nhanvien_create(request):
    """POST: Tạo nhân viên mới"""
    data = request.data
    try:
        obj = NhanVienService.create(
            ho_ten=data.get('ho_ten'),
            ma_chuc_vu=data.get('ma_chuc_vu'),
            sdt=data.get('sdt'),
            dia_chi=data.get('dia_chi')
        )
    except ValueError as e:
        return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    serializer = NhanVienSerializer(obj)
    return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['PUT'])
def nhanvien_update(request, ma_nv):
    """PUT: Cập nhật nhân viên"""
    try:
        obj = NhanVienService.update(ma_nv, **request.data)
    except ValueError as e:
        return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    if not obj:
        return Response({"detail": "Nhân viên không tồn tại"}, status=status.HTTP_404_NOT_FOUND)
    serializer = NhanVienSerializer(obj)
    return Response(serializer.data)

@api_view(['DELETE'])
def nhanvien_delete(request, ma_nv):
    """DELETE: Xóa nhân viên"""
    success = NhanVienService.delete(ma_nv)
    if not success:
        return Response({"detail": "Nhân viên không tồn tại"}, status=status.HTTP_404_NOT_FOUND)
    return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
def nhanvien_search(request):
    keyword = request.query_params.get('keyword')

    if not keyword:
        return Response(
            {"detail": "Vui lòng cung cấp keyword"},
            status=400
        )

    nhan_viens = NhanVienService.search(keyword)
    serializer = NhanVienSerializer(nhan_viens, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def nhanvien_filter_by_chucvu(request):
    """GET: Lọc nhân viên theo chức vụ"""
    chucvu_id = request.query_params.get('chucvu_id')
    if not chucvu_id:
        return Response({"detail": "Vui lòng cung cấp chucvu_id"}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        queryset = NhanVienService.filter_by_chuc_vu(int(chucvu_id))
    except ValueError:
        return Response({"detail": "chucvu_id phải là số nguyên"}, status=status.HTTP_400_BAD_REQUEST)
    
    serializer = NhanVienSerializer(queryset, many=True)
    return Response(serializer.data)


# ViewSet cho NhanVien
class NhanVienViewSet(viewsets.ViewSet):

    # GET /api/nhanvien/
    def list(self, request):
        queryset = NhanVienService.list_all()
        serializer = NhanVienSerializer(queryset, many=True)
        return Response(serializer.data)

    # GET /api/nhanvien/{id}/
    def retrieve(self, request, pk=None):
        obj = NhanVienService.get(int(pk))
        if not obj:
            return Response({"detail": "Nhân viên không tồn tại"}, status=status.HTTP_404_NOT_FOUND)
        serializer = NhanVienSerializer(obj)
        return Response(serializer.data)

    # POST /api/nhanvien/
    def create(self, request):
        data = request.data
        try:
            obj = NhanVienService.create(
                ho_ten=data.get('ho_ten'),
                ma_chuc_vu=data.get('ma_chuc_vu'),
                sdt=data.get('sdt'),
                dia_chi=data.get('dia_chi')
            )
        except ValueError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        serializer = NhanVienSerializer(obj)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    # PUT /api/nhanvien/{id}/
    def update(self, request, pk=None):
        try:
            obj = NhanVienService.update(int(pk), **request.data)
        except ValueError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        if not obj:
            return Response({"detail": "Nhân viên không tồn tại"}, status=status.HTTP_404_NOT_FOUND)
        serializer = NhanVienSerializer(obj)
        return Response(serializer.data)

    # DELETE /api/nhanvien/{id}/
    def destroy(self, request, pk=None):
        success = NhanVienService.delete(int(pk))
        if not success:
            return Response({"detail": "Nhân viên không tồn tại"}, status=status.HTTP_404_NOT_FOUND)
        return Response(status=status.HTTP_204_NO_CONTENT)

    # GET /api/nhanvien/search/?q=keyword
    @action(detail=False, methods=['get'])
    def search(self, request):
        q = request.query_params.get('q', '')
        queryset = NhanVienService.find_by_name(q)
        serializer = NhanVienSerializer(queryset, many=True)
        return Response(serializer.data)

    # GET /api/nhanvien/filter_by_chucvu/?chucvu_id=1
    @action(detail=False, methods=['get'])
    def filter_by_chucvu(self, request):
        chucvu_id = request.query_params.get('chucvu_id')
        if not chucvu_id:
            return Response({"detail": "Vui lòng cung cấp chucvu_id"}, status=status.HTTP_400_BAD_REQUEST)
        queryset = NhanVienService.filter_by_chuc_vu(int(chucvu_id))
        serializer = NhanVienSerializer(queryset, many=True)
        return Response(serializer.data)

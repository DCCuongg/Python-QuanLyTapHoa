from rest_framework import serializers
from QuanLyHangHoa.models.hang_hoa import HangHoa

class HangHoaSerializer(serializers.ModelSerializer):
    class Meta:
        model = HangHoa
        fields = '__all__'
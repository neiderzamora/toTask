from rest_framework import serializers
from evidence.models import *

class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = '__all__'

class EvidenceSerializer(serializers.ModelSerializer):
    archivos = FileSerializer(many=True, required=False)
    date_upload = serializers.DateTimeField(format='%Y-%m-%e %H:%M', read_only=True)
    user = serializers.SlugRelatedField(
        slug_field='email',
        queryset=CustomUser.objects.all()
    )
    task = serializers.SlugRelatedField(
        slug_field='name',
        queryset=Task.objects.all()
    )

    class Meta:
        model = Evidence
        fields = '__all__'
        read_only_fields = ['id', 'date_upload']


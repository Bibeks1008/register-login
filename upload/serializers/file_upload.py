from rest_framework import serializers
from upload.models.file_upload import File

class FileUploadSerializer(serializers.ModelSerializer):
    file = serializers.FileField(write_only=True)

    class Meta:
        model = File
        fields = ["id", "user", "file", "file_path"]

    read_only_fields = ["file_path"]

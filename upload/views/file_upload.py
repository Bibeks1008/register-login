from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response

from upload.serializers.file_upload import FileUploadSerializer
from upload.services.file_service import FileService
from Abstraction.builders.response_builder import ResponseBuilder

class FileUploadCreateView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    serializer_class = FileUploadSerializer

    def post(self, request, *args, **kwargs):
        response_builder = ResponseBuilder()
        user = request.user
        file = request.FILES.get("file")

        if not file:
            return (
                response_builder.result_object({})
                .fail()
                .message("File not provided")
                .get_response()
            )

        try:
            # Create file upload record in database
            file_upload = FileService.create_file_upload(user=user, file=file)
            serializer = FileUploadSerializer(file_upload)
            return (
                response_builder.result_object(serializer.data)
                .success()
                .message("File uploaded successfully")
                .get_response()
            )
        except Exception as e:
            return (
                response_builder.result_object({"error": str(e)})
                .fail()
                .internal_error_500()
                .message(str(e))
                .get_response()
            )

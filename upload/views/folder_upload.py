from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response

from upload.services.file_service import FileService
from Abstraction.builders.response_builder import ResponseBuilder
from rest_framework.exceptions import ValidationError
from upload.serializers.file_upload import FileUploadSerializer

from shared.helpers.logging_helper import logger

class FolderUploadCreateView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    serializer_class = FileUploadSerializer 

    def post(self, request, *args, **kwargs):
        response_builder = ResponseBuilder()
        user = request.user

        files = request.FILES.getlist('files')
        paths = request.POST.getlist('paths')

        if not files or not paths:
            return response_builder.result_object({}).fail().message("No files or paths uploaded").get_response()

        if len(files) != len(paths):
            raise ValidationError("Mismatch between files and paths")

        try:
            uploaded_files_urls = FileService.create_folder_upload(user=user, files=files, paths=paths)

            return response_builder.result_object({"file_urls": uploaded_files_urls}).success().message("Folder uploaded successfully!").get_response()

        except Exception as e:
            logger.error(f"Error during file upload: {str(e)}")
            logger.exception(e)
            return response_builder.result_object({"error": str(e)}).fail().internal_error_500().message(str(e)).get_response()



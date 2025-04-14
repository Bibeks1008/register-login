from upload.models.file_upload import File
from upload.services.storage_service import StorageService
from Abstraction.exception import ServiceError

class FileService:
    @staticmethod
    def create_file_upload(user, file):
        """
        Create a FileUpload instance and store the file.
        """
        try:
            # Save the file using StorageService
            file_path = StorageService.save_file(file=file, file_name=file.name)
            uploaded_file = File(user=user, file_path=file_path)
            uploaded_file.save()  # Save the FileUpload instance
            return uploaded_file
        except Exception as e:
            raise ServiceError("Error occurred while uploading the file: " + str(e))

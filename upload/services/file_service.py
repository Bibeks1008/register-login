from upload.models.file_upload import File
from upload.services.storage_service import StorageService
from Abstraction.exception import ServiceError
from shared.helpers.logging_helper import logger

class FileService:
    @staticmethod
    def create_file_upload(user, file):
        """
        Create a FileUpload instance and store the file.
        """
        try:
            # Save the file using StorageService
            file_url = StorageService.save_single_file(file=file, file_name=file.name)
            uploaded_file = File(user=user, name=file.name, file_url=file_url)
            uploaded_file.save() 
            return uploaded_file
        except Exception as e:
            raise ServiceError("Error occurred while uploading the file: " + str(e))


    @staticmethod
    def create_folder_upload(user, files, paths):
        try:
            file_urls = []  
            for file, relative_path in zip(files, paths):
                logger.info(f"Saving file {file.name} as {relative_path}")

                file_url = StorageService.save_file_in_folder(file, relative_path)

                uploaded_file  = File(user=user, name=file.name, file_url=file_url, relative_path=relative_path)
                uploaded_file.save()
                
                file_urls.append(file_url)

        except Exception as e:
            raise ServiceError(f"Error occurred while uploading the files: {str(e)}")

        return file_urls
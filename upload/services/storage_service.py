import os
from django.conf import settings
from django.core.files.storage import FileSystemStorage

from shared.helpers.logging_helper import logger

class StorageService:
    @staticmethod
    def save_single_file(file, file_name):
        # Using the default file storage to handle file saving
        fs = FileSystemStorage(location=settings.MEDIA_ROOT, base_url=settings.MEDIA_URL)
        file_name = fs.save(os.path.join("uploads", file_name), file)  
        file_url = fs.url(file_name) 
        full_url = f"{settings.BASE_URL}{file_url}" if settings.BASE_URL else file_url
        return full_url

    
    @staticmethod
    def save_file_in_folder(file, relative_path):
        # Normalize the relative path to remove '../', './', etc.
        normalized_path = os.path.normpath(relative_path).replace("\\", "/")

        # Prevent path traversal outside MEDIA_ROOT
        if normalized_path.startswith("..") or os.path.isabs(normalized_path):
            raise SuspiciousOperation("Invalid file path: potential directory traversal detected.")

        # Construct the full absolute path to save the file
        full_path = os.path.join(settings.MEDIA_ROOT, normalized_path)

        # Ensure the path is still inside MEDIA_ROOT
        media_root_abs = os.path.abspath(settings.MEDIA_ROOT)
        full_path_abs = os.path.abspath(full_path)
        if not full_path_abs.startswith(media_root_abs):
            raise SuspiciousOperation("Attempt to save file outside of MEDIA_ROOT.")

        # Create directories if they don't exist
        os.makedirs(os.path.dirname(full_path_abs), exist_ok=True)

        # Save the file
        with open(full_path_abs, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)

        file_url = os.path.join(settings.MEDIA_URL, normalized_path).replace("\\", "/")
        full_url = f"{settings.BASE_URL}{file_url}" if getattr(settings, 'BASE_URL', None) else file_url

        return full_url

from django.conf import settings
from django.core.files.storage import FileSystemStorage
import os

class StorageService:
    @staticmethod
    def save_file(file, file_name):
        """
        Save any file and return its URL.
        """
        # Using the default file storage to handle file saving
        fs = FileSystemStorage(location=settings.MEDIA_ROOT, base_url=settings.MEDIA_URL)
        file_name = fs.save(os.path.join("uploads", file_name), file)  
        file_url = fs.url(file_name) 
        full_url = f"{settings.BASE_URL}{file_url}" if settings.BASE_URL else file_url
        return full_url

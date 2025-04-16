from django.urls import path, include

from upload.views.file_upload import FileUploadCreateView
from upload.views.folder_upload import FolderUploadCreateView

app_name = 'file'

urlpatterns=[
    path('api/file-upload/', FileUploadCreateView.as_view(), name='file_upload'),
    path('api/upload-directory/', FolderUploadCreateView.as_view(), name='upload_directory'),
]
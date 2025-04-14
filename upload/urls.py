from django.urls import path, include

from upload.views.file import FileUploadCreateView

app_name = 'file'

urlpatterns=[
    path('api/file-upload/', FileUploadCreateView.as_view(), name='file_upload'),
   
]
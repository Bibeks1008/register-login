from django.db import models
from user.models.user import User

class File(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    # file = models.FileField(upload_to="uploads/", null=True, blank=True)
    file_url = models.URLField(max_length=500, blank=True, null=True)
    relative_path = models.CharField(max_length=512, blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"File {self.id} - {self.user.username}"

from django.db import models
from user.models.user import User

class File(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.FileField(upload_to="uploads/", null=True, blank=True)
    file_path = models.URLField(max_length=500, blank=True, null=True)
    
    def __str__(self):
        return f"File {self.id} - {self.user.username}"

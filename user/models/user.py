from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid

from user.constants import ROLE_CHOICES, User
# Create your models here.

class User(AbstractUser):
    idx= models.UUIDField(default=uuid.uuid4, editable=False, unique=True, primary_key=True)
    # email_verified= models.BooleanField(default=False,)
    role= models.CharField(max_length=25, choices=ROLE_CHOICES, default="User")
    created_at= models.DateTimeField(auto_now_add=True)
    updated_at= models.DateTimeField(auto_now=True)
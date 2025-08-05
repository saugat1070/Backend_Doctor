from django.db import models
import uuid
from Authentication.models import User

# Create your models here.

class DoctorModel(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, primary_key=True)
    name_doctor = models.CharField(max_length=20, null=False)
    core_education = models.CharField(max_length=100, null=False)
    topic_education = models.CharField(max_length=100, null=False)
    experience = models.IntegerField(default=0)
    about = models.TextField(null=True, blank=True)
    appoint_fee = models.IntegerField(default=0)
    is_available = models.BooleanField(default=True)
    profile_doctor = models.ImageField(upload_to="storage/")
    createdBy = models.ForeignKey(User, on_delete=models.CASCADE, related_name='doctors')
    
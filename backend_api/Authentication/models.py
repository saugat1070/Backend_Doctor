from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
import random
import uuid

# Create your models here.

Role = (
    ("admin","Admin"),
    ("doctor","Doctor"),
    ("patient","Patient")
)

class UserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, first_name=first_name, last_name=last_name,**extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        first_name = extra_fields.pop('first_name', 'Admin')
        last_name = extra_fields.pop('last_name', 'User')

        return self.create_user(email, first_name=first_name, last_name=last_name, password=password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, primary_key=True)
    email = models.EmailField(unique=True, null=False)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    photo_name = models.ImageField(upload_to='photos/', height_field=None, width_field=None, null=True, blank=True)
    username = models.CharField(max_length=8, unique=True, blank=True) 
    date_of_birth = models.DateField(null=True, blank=True)
    role = models.CharField(default="patient",choices=Role)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False) 
    otp = models.CharField(max_length=6, blank=True, null=True)
    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]  

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        if not self.username:
            self.username = self.get_username()
        super().save(*args, **kwargs)

    def get_username(self):
        username = f'{self.first_name[:4]}{random.randint(1,9)}'.lower()
        return username

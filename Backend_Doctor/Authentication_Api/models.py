from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.utils import timezone
# Create your models here.

class UserRegistrationManager(BaseUserManager):
    def create_user(self,email,name,password=None,**extra_fields):
        if not email:
            raise ValueError("User must have email address")
        
        user = self.model(
            email = self.normalize_email(email),
            name = name,
            **extra_fields,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, name, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_admin',True)
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError("Superuser must have is_staff=True")
        
        if extra_fields.get('is_superuser') is not True:
            raise ValueError("Superuser must have is_superuser=True")
        
        user = self.create_user(
            email=email,
            name=name,
            password=password,
            **extra_fields
        )
        return user
    
class UserRegistration(AbstractBaseUser):
    email = models.EmailField(max_length=225,unique=True)
    name = models.CharField(max_length=20)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    choose = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ]
    profile_picture = models.ImageField(upload_to='photo/',null=True)
    gender = models.CharField(choices=choose,default='male',null=True)
    phone_number = models.BigIntegerField(null=True)
    created_at = models.DateTimeField(default=timezone.now)
    date_of_birth = models.DateField(null=True)
    
    
    objects = UserRegistrationManager()
    
    USERNAME_FIELD ='email'
    REQUIRED_FIELDS = ['name']
    
    def __str__(self):
        return self.email
    
    def has_perm(self,perm,obj=None):
        return self.is_superuser
    
    def has_module_perms(self,app_label):
        return self.is_superuser
    

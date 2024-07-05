from django.db import models


from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.shortcuts import get_object_or_404
# Create your models here.
class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        if password:
            user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password=password, **extra_fields)

class movieuser(AbstractBaseUser):
    username = models.CharField(max_length=30,null= True,unique=True)
    email = models.EmailField(max_length=50, unique=True)
    firstname = models.CharField(max_length=25,null= True,unique=True)
    lastname = models.CharField(max_length=10, null=True)
    password = models.CharField(max_length=20,null=True)
    description=models.CharField(max_length=200,null=True)
    profilepic=models.ImageField(upload_to='media',default='media/noneimage.jpg')
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['firstname', 'lastname', 'email','password']

    def has_module_perms(self, app_label):
        return True
    def has_perm(self, perm, obj=None):
        return True
    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        
        super().save(*args, **kwargs)



class Category(models.Model):
    id=models.AutoField(primary_key=True)
    category_name=models.CharField(max_length=200)

    def __str__(self):
        return self.category_name
    

class movielist(models.Model):
    title=models.CharField(max_length=200)
    addeduser=models.ForeignKey(movieuser,on_delete=models.CASCADE)
    poster=models.ImageField(upload_to='media')
    description=models.CharField(max_length=200)
    Language=models.CharField(max_length=200,default='English')
    release_date=models.DateField(null=True,blank=True)
    actors=models.CharField(max_length=200)
    category=models.ForeignKey(Category,on_delete=models.CASCADE)
    trailerlink=models.URLField()
    rating=models.PositiveIntegerField(null=True,blank=True)
    reviews=models.CharField(max_length=200)

    def __str__(self):
        return self.title

from random import choices
from django.db import models
from datetime import timedelta
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.conf import settings
import datetime
# Create your models here.
from django.utils.translation import gettext_lazy as _



class GeneratedQuestionSet(models.Model):
    name = models.CharField(max_length=255)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)    
    created_at = models.DateTimeField(auto_now_add=True)
    
class GeneratedQuestion(models.Model):
    question_text = models.TextField(null=True)
    question_set = models.ForeignKey(GeneratedQuestionSet,null=True,  on_delete=models.CASCADE)


class CustomUserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    def _create_user(self, email, password=None, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)

class CustomUser(AbstractUser):
    
    username = None
    email = models.EmailField(_('email address'), unique=True)
    mobile = models.CharField(max_length=15, null=True, blank= True)
    is_verified = models.BooleanField(default=False)
    forget_password = models.CharField(max_length=255, blank= True, null=True)
    
    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = ['mobile']

    objects = CustomUserManager()

    def __str__(self):
        return self.first_name


# class CustomUser(AbstractUser):
#     username = None
#     email = models.EmailField(_('email address'), unique=True)

#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = []

#     objects = CustomUserManager()
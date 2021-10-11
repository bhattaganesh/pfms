from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager   

# Create your models here.

class UserManager(BaseUserManager):
    def create_user(self, email, name, password=None):
        user = self.model(
            email = self.normalize_email(email),
            name = name,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password=None):
        user = self.create_user(email,name, password)
        user.is_admin = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    
    email = models.EmailField(max_length=50, unique=True, verbose_name="Email")
    name = models.CharField(max_length=30)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"

    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True
    
    @property
    def is_staff(self):
        return self.is_admin

from django.db import models
from django.db.models.deletion import CASCADE
from authentication.models import User

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, related_name="user_profile", on_delete=CASCADE)
    avatar = models.ImageField(upload_to='users/profiles/avatars', null=True, blank=True)
    gender = models.CharField(max_length=20 ,null=True, blank=True)
    birthday = models.DateField(null=True, blank=True)
    phone = models.CharField(max_length=32, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.email+" - profile"
    

    class Meta:
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'
    
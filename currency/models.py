from django.db import models
from authentication.models import User

# Create your models here.
class Currency(models.Model):
    currency = models.CharField(max_length=255, blank=True, null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return  str(self.user.email)+"'s "+self.currency

    
    class Meta:
        verbose_name_plural = 'Currencies'
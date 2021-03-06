from django.db import models
from django.db.models.deletion import CASCADE, SET_DEFAULT
from authentication.models import User
# from django.utils.timezone import now

# Create your models here.
class IncomeCategory(models.Model):
    title = models.CharField(max_length=150)
    description = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey(to=User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
    class Meta:
        verbose_name_plural = 'incomeCategories'
        unique_together = ('title', 'created_by')

class Income(models.Model):
    amount = models.FloatField()
    description = models.TextField(blank=True, null=True)
    income_by = models.ForeignKey(User, on_delete=models.CASCADE)
    # income_category = models.ForeignKey(IncomeCategory, on_delete=models.SET_NULL, null=True)
    income_category = models.ForeignKey(IncomeCategory,default=1, on_delete=SET_DEFAULT)
    income_date = models.DateField()
    # entry_date = models.DateField(default=now)
    entry_date = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    def __str__(self):
        return f"{self.amount} - {self.income_by.email}"

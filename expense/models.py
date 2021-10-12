from django.db import models
from authentication.models import User
from django.utils.timezone import now

# Create your models here.
class ExpenseCategory(models.Model):
    title = models.CharField(max_length=150)
    description = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey(to=User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
    class Meta:
        verbose_name_plural = 'ExpenseCategories'
        unique_together = ('title', 'created_by')

class Expense(models.Model):
    amount = models.FloatField()
    description = models.TextField(blank=True, null=True)
    expense_by = models.ForeignKey(User, on_delete=models.CASCADE)
    expense_category = models.ForeignKey(ExpenseCategory, on_delete=models.SET_NULL, null=True)
    expense_date = models.DateField()
    entry_date = models.DateField(default=now)

    def __str__(self):
        return self.expense_category.title
    

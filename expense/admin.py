from django.contrib import admin
from .models import Expense, ExpenseCategory

# Register your models here.
class ExpenseAdmin(admin.ModelAdmin):
    list_display = (
        'amount',
        'description',
        'expense_by',
        'expense_category',
        'expense_date',
        'entry_date',
        'updated_at',
    )

    search_fields = (
        'amount',
        'description',
        'expense_by',
        'expense_category',
        'expense_date',
        'entry_date',
        'updated_at',
    )
    list_per_page = 5

class ExpenseCategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'description')
    search_fields = ('title', 'description')
    list_per_page = 5


admin.site.register(Expense, ExpenseAdmin)
admin.site.register(ExpenseCategory, ExpenseCategoryAdmin)

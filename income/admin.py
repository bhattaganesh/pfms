from django.contrib import admin

from income.models import Income, IncomeCategory

# Register your models here.
class IncomeAdmin(admin.ModelAdmin):
    list_display = (
        'amount',
        'description',
        'income_by',
        'income_category',
        'income_date',
        'entry_date',
        'updated_at',
    )

    search_fields = (
        'amount',
        'description',
        'income_by',
        'income_category',
        'income_date',
        'entry_date',
        'updated_at',
    )

    list_per_page = 5
class IncomeCategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'description')
    search_fields = ('title', 'description')
    list_per_page = 5



admin.site.register(Income, IncomeAdmin)
admin.site.register(IncomeCategory, IncomeCategoryAdmin)
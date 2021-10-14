from django.contrib import admin

from income.models import Income, IncomeCategory

# Register your models here.
admin.site.register([Income, IncomeCategory])
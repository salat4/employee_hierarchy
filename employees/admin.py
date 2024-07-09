from django.contrib import admin
from .models import Employee

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('name', 'position', 'hire_date', 'email', 'manager')
    search_fields = ('name', 'position', 'email')
    list_filter = ('position', 'hire_date')

from django.shortcuts import render
from .models import Employee

def employee_hierarchy(request):
    employees = Employee.objects.filter(manager__isnull=True).prefetch_related('subordinates')
    return render(request, 'employees/hierarchy.html', {'employees': employees})

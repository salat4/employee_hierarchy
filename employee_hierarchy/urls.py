from django.contrib import admin
from django.urls import path
from employees import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.employee_hierarchy, name='employee_hierarchy'),
]

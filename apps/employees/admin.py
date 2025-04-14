from django.contrib import admin
from .models import Department, Employee

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'position', 'department', 'status')
    list_filter = ('status', 'department', 'hire_date')
    search_fields = ('first_name', 'last_name', 'email')
    date_hierarchy = 'hire_date'
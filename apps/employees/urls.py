from django.urls import path
from .views import (
    EmployeeListView, EmployeeDetailView, EmployeeCreateView,
    EmployeeUpdateView, EmployeeDeleteView, generate_report,
    export_csv, dashboard
)

urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('employees/', EmployeeListView.as_view(), name='employee-list'),
    path('employees/<int:pk>/', EmployeeDetailView.as_view(), name='employee-detail'),
    path('employees/create/', EmployeeCreateView.as_view(), name='employee-create'),
    path('employees/<int:pk>/update/', EmployeeUpdateView.as_view(), name='employee-update'),
    path('employees/<int:pk>/delete/', EmployeeDeleteView.as_view(), name='employee-delete'),
    path('employees/<int:pk>/report/', generate_report, name='generate-report'),
    path('employees/export-csv/', export_csv, name='export-csv'),
]
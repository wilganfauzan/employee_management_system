import logging
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.utils import timezone
from django.http import HttpResponse
from .models import Employee, Department
from .tasks import send_welcome_email, generate_employee_report, export_employees_csv

logger = logging.getLogger(__name__)


class EmployeeListView(ListView):
    model = Employee
    template_name = 'employees/employee_list.html'
    context_object_name = 'employees'
    paginate_by = 10


class EmployeeDetailView(DetailView):
    model = Employee
    template_name = 'employees/employee_detail.html'
    context_object_name = 'employee'


class EmployeeCreateView(CreateView):
    model = Employee
    template_name = 'employees/employee_form.html'
    fields = ['first_name', 'last_name', 'email', 'department', 'position', 'hire_date', 'status', 'salary']
    success_url = reverse_lazy('employee-list')

    def form_valid(self, form):
        response = super().form_valid(form)
        # Queue welcome email task
        send_welcome_email(self.object.id)
        messages.success(self.request, f"Employee {self.object} created. Welcome email queued.")
        return response


class EmployeeUpdateView(UpdateView):
    model = Employee
    template_name = 'employees/employee_form.html'
    fields = ['first_name', 'last_name', 'email', 'department', 'position', 'status', 'salary']
    success_url = reverse_lazy('employee-list')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f"Employee {self.object} updated successfully.")
        return response


class EmployeeDeleteView(DeleteView):
    model = Employee
    template_name = 'employees/employee_confirm_delete.html'
    success_url = reverse_lazy('employee-list')

    def delete(self, request, *args, **kwargs):
        employee = self.get_object()
        messages.success(request, f"Employee {employee} deleted successfully.")
        return super().delete(request, *args, **kwargs)


def generate_report(request, pk):
    """Generate employee report and queue it as a background task"""
    employee = get_object_or_404(Employee, pk=pk)

    # Queue the report generation task
    task_id = generate_employee_report(employee.id)

    messages.success(request, f"Report generation for {employee} has been queued.")
    return redirect('employee-detail', pk=pk)


def export_csv(request):
    """Export all employees to CSV using a background task"""
    # Queue the export task
    result = export_employees_csv()

    # Create response with CSV data
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="employees.csv"'
    response.write(result)

    return response


def dashboard(request):
    """Simple dashboard with employee statistics"""
    total_employees = Employee.objects.count()
    active_employees = Employee.objects.filter(status='active').count()
    departments = Department.objects.all()

    context = {
        'total_employees': total_employees,
        'active_employees': active_employees,
        'departments': departments,
    }

    return render(request, 'employees/dashboard.html', context)
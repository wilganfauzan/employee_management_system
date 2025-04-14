import csv
import io
import logging
from datetime import datetime, timedelta
from huey import crontab
from huey.contrib.djhuey import task, periodic_task, db_task
from django.core.mail import send_mail
from django.utils import timezone
from django.conf import settings
from .models import Employee, Department

logger = logging.getLogger(__name__)


@task()
def send_welcome_email(employee_id):
    """Send welcome email to new employees"""
    try:
        employee = Employee.objects.get(id=employee_id)
        logger.info(f"Sending welcome email to {employee.email}")
        # In production, this would send an actual email
        logger.info(f"Email sent to {employee.email} with subject 'Welcome to our company!'")
        return f"Welcome email sent to {employee.email}"
    except Employee.DoesNotExist:
        logger.error(f"Employee with id {employee_id} does not exist")
        return f"Error: Employee with id {employee_id} not found"


@db_task()
def generate_employee_report(employee_id):
    """Generate performance report for an employee"""
    try:
        employee = Employee.objects.get(id=employee_id)
        logger.info(f"Generating report for {employee}")
        # Simulate report generation
        employee.last_report_generated = timezone.now()
        employee.save()
        logger.info(f"Report generated for {employee}")
        return f"Report generated for {employee.first_name} {employee.last_name}"
    except Employee.DoesNotExist:
        logger.error(f"Employee with id {employee_id} does not exist")
        return f"Error: Employee with id {employee_id} not found"


@periodic_task(crontab(hour='0', minute='0'))
def daily_department_report():
    """Generate daily department report"""
    logger.info("Generating daily department report")
    departments = Department.objects.all()
    report = []

    for dept in departments:
        active_count = dept.employees.filter(status='active').count()
        on_leave_count = dept.employees.filter(status='on_leave').count()
        report.append({
            'department': dept.name,
            'active_employees': active_count,
            'on_leave_employees': on_leave_count,
            'total_employees': active_count + on_leave_count
        })

    logger.info(f"Daily department report generated: {report}")
    return report


@periodic_task(crontab(day_of_week='1', hour='9', minute='0'))
def weekly_salary_report():
    """Generate weekly salary report"""
    logger.info("Generating weekly salary report")

    departments = Department.objects.all()
    report = []

    for dept in departments:
        employees = dept.employees.filter(status='active')
        total_salary = sum(employee.salary for employee in employees)
        avg_salary = total_salary / employees.count() if employees.count() > 0 else 0

        report.append({
            'department': dept.name,
            'total_salary': total_salary,
            'average_salary': avg_salary,
            'employee_count': employees.count()
        })

    logger.info(f"Weekly salary report generated: {report}")
    return report


@task()
def export_employees_csv():
    """Export all employees to CSV"""
    logger.info("Exporting employees to CSV")

    output = io.StringIO()
    writer = csv.writer(output)

    # Write header
    writer.writerow(['ID', 'First Name', 'Last Name', 'Email', 'Department',
                     'Position', 'Hire Date', 'Status', 'Salary'])

    # Write employee data
    for employee in Employee.objects.all():
        writer.writerow([
            employee.id,
            employee.first_name,
            employee.last_name,
            employee.email,
            employee.department.name if employee.department else '',
            employee.position,
            employee.hire_date,
            employee.status,
            employee.salary
        ])

    logger.info("CSV export completed")
    return output.getvalue()
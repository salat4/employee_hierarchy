from django.core.management.base import BaseCommand
from employees.models import Employee
import datetime
import random


class Command(BaseCommand):
    help = 'Seed the database with 50000 employee data'

    def handle(self, *args, **kwargs):
        # Видалити всі старі записи порційно
        batch_size = 1000
        qs = Employee.objects.all()
        while qs.exists():
            ids = list(qs.values_list('id', flat=True)[:batch_size])
            Employee.objects.filter(id__in=ids).delete()
        self.stdout.write(self.style.WARNING('Old employee records deleted.'))

        def create_employees(manager, num_employees, position_prefix):
            employees = []
            for i in range(num_employees):
                employee = Employee(
                    name=f'{position_prefix}_{i + 1}_{manager.position}_{manager.id}',
                    position=f'{position_prefix}',
                    hire_date=datetime.date(2000 + random.randint(1, 20), random.randint(1, 12), random.randint(1, 28)),
                    email=f'{position_prefix.lower()}_{i + 1}@example.com',
                    manager=manager
                )
                employees.append(employee)
                # Записувати в базу даних частинами
                if len(employees) >= 1000:
                    Employee.objects.bulk_create(employees)
                    employees = []
            if employees:
                Employee.objects.bulk_create(employees)
            return Employee.objects.filter(manager=manager, position=position_prefix)

        total_employees = 50000
        created_employees = 0

        # Create CEO
        ceo = Employee.objects.create(
            name='CEO',
            position='CEO',
            hire_date=datetime.date(2000, 1, 1),
            email='ceo@example.com',
            manager=None
        )
        created_employees += 1

        # Create C-level employees
        c_levels = ['CFO', 'COO', 'CTO', 'CMO']
        c_level_managers = []
        for c_level in c_levels:
            manager = Employee.objects.create(
                name=c_level,
                position=c_level,
                hire_date=datetime.date(2001, 1, 1),
                email=f'{c_level.lower()}@example.com',
                manager=ceo
            )
            c_level_managers.append(manager)
            created_employees += 1

        # Create Directors
        positions = {
            'COO': ['Director of Operations'],
            'CFO': ['Director of Accounting'],
            'CTO': ['Director of IT'],
            'CMO': ['Director of Communications']
        }
        director_managers = []
        for manager in c_level_managers:
            position_list = positions[manager.position]
            for position in position_list:
                director = Employee.objects.create(
                    name=position,
                    position=position,
                    hire_date=datetime.date(2002, 1, 1),
                    email=f'{position.lower().replace(" ", "_")}@example.com',
                    manager=manager
                )
                director_managers.append(director)
                created_employees += 1

        # Create TeamLeads
        teamlead_positions = {
            'Director of Operations': ['TeamLead of Presale', 'TeamLead of Safeguard', 'TeamLead of Account'],
            'Director of Accounting': ['TeamLead of Finance', 'TeamLead of Business Analytics',
                                       'TeamLead of Accountant'],
            'Director of IT': ['TeamLead of Front-end', 'TeamLead of Back-end', 'TeamLead of DEVOPS', 'TeamLead of QA'],
            'Director of Communications': ['TeamLead of Design', 'TeamLead of Marketing', 'TeamLead of Targeting',
                                           'TeamLead of LeadGeneration']
        }
        teamlead_managers = []
        for manager in director_managers:
            position_list = teamlead_positions[manager.position]
            for position in position_list:
                teamlead = Employee.objects.create(
                    name=position,
                    position=position,
                    hire_date=datetime.date(2003, 1, 1),
                    email=f'{position.lower().replace(" ", "_")}@example.com',
                    manager=manager
                )
                teamlead_managers.append(teamlead)
                created_employees += 1

        # Create PMs
        pm_managers = []
        for teamlead in teamlead_managers:
            pm_managers += create_employees(teamlead, 10, 'PM')
        created_employees += len(pm_managers)

        # Create Seniors
        senior_managers = []
        for pm in pm_managers:
            senior_managers += create_employees(pm, 10, 'Senior')
        created_employees += len(senior_managers)

        # Calculate remaining employees to be assigned as Employees
        remaining_employees = total_employees - created_employees
        employee_batches = remaining_employees // len(senior_managers)
        extra_employees = remaining_employees % len(senior_managers)

        for senior in senior_managers:
            num_employees_to_create = employee_batches + (1 if extra_employees > 0 else 0)
            create_employees(senior, num_employees_to_create, 'Employee')
            created_employees += num_employees_to_create
            if extra_employees > 0:
                extra_employees -= 1

        self.stdout.write(self.style.SUCCESS(f'Database seeded successfully with {created_employees} employees.'))

from django.core.management.base import BaseCommand
from django_seed import Seed
from ...models import Employee
import datetime

class Command(BaseCommand):
    help = 'Seed the database with employee data'

    def handle(self, *args, **kwargs):
        seeder = Seed.seeder()
        ceo = Employee.objects.create(
            name='CEO',
            position='CEO',
            hire_date=datetime.date(2000, 1, 1),
            email='ceo@example.com',
            manager=None
        )

        def create_subordinates(manager, level):
            if level <= 0:
                return
            for i in range(5):
                subordinate = Employee.objects.create(
                    name=f'Employee_Level_{7-level}_{i}',
                    position='Employee',
                    hire_date=datetime.date(2020-level, 1, 1),
                    email=f'employee_{7-level}_{i}@example.com',
                    manager=manager
                )
                create_subordinates(subordinate, level-1)

        for i in range(5):
            manager = Employee.objects.create(
                name=f'Manager_Level_1_{i}',
                position='Manager',
                hire_date=datetime.date(2001, 1, 1),
                email=f'manager1_{i}@example.com',
                manager=ceo
            )
            create_subordinates(manager, 6)

        self.stdout.write(self.style.SUCCESS('Database seeded successfully.'))

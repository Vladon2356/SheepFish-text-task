import random
import uuid

from apps.check.models import Check
from apps.printer.models import Printer

# here can be installed Faker library and generate fake data
# but I decided to use just library random

point_ids = range(1, 11)
products = ['milk', 'meet', 'fish', 'apple', 'coca cola', 'pepsi', 'tomato', 'rice', 'potato', 'carrot', 'onion']


def create_printers_for_point(point_id):
    Printer.objects.create(
        name=f'Printer {random.randint(1, 100)}',
        api_key=f'api_key_{point_id}',
        point_id=point_id,
        check_type='client'
    )
    Printer.objects.create(
        name=f'Printer {random.randint(1, 100)}',
        api_key=f'api_key_{random.randint(1, 100)}',
        point_id=point_id,
        check_type='kitchen'
    )


def create_check(printer_id):
    order = {
        'order_number': uuid.uuid4().hex,
        'point_id': random.choice(point_ids),
    }
    for i in range(random.randint(1, 10)):
        product = random.choice(products)
        order[product] = random.randint(1, 5)
    Check.objects.create(
        printer_id=printer_id,
        order=order,
    )


def populate_db(count_printers=11, count_checks=101):
    for i in range(1, count_printers):
        create_printers_for_point(point_id=i)
    for i in range(1, count_checks):
        create_check(printer_id=random.randint(1, 2*count_printers-1))

from core.celery import app

from apps.check.models import Check
from apps.check.services import generate_pdf_for_check


@app.task
def generate_pdf_for_check_task(check_id):
    try:
        check = Check.objects.get(id=check_id)
        return generate_pdf_for_check(check)
    except Exception as e:
        print(e)

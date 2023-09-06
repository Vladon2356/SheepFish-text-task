from core.celery import app

from apps.check.services import generate_pdf_for_check


@app.task
def generate_pdf_for_check_task(data):
    try:
        print('generate_pdf_for_check_task')
        generate_pdf_for_check(data)
    except Exception as e:
        print(e)

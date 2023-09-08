import json
import requests
import codecs
from django.template.loader import render_to_string
from core.settings import MEDIA_ROOT

URL = 'http://wkhtmltopdf:80/'
HEADERS = {
    'Content-Type': 'application/json',
}


def generate_pdf_for_check(check):
    html_content = render_to_string('check.html', {'check': check})
    data = {
        'contents': codecs.encode(html_content.encode(), 'base64').decode(),
    }
    response = requests.post(URL, data=json.dumps(data, ensure_ascii=True), headers=HEADERS)

    file_name = f'{check.order.get("order_number")}_{check.type}.pdf'

    if response.status_code == 200:
        pdf_filepath = f'{MEDIA_ROOT}/pdf/{file_name}'
        with open(pdf_filepath, 'wb') as f:
            f.write(response.content)
        return file_name
    else:
        raise Exception(f"Error generating PDF: {response.status_code} - {response.text}")

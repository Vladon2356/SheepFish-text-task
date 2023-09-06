import json
import requests
from django.template.loader import render_to_string
from core.settings import MEDIA_ROOT

URL = 'http://localhost:8080/'
HEADERS = {
    'Content-Type': 'application/json',
}


def generate_pdf_for_check(check_data):
    print('check_data', check_data)
    # Render the HTML content
    html_content = render_to_string('check.html', {'data': check_data})

    html_filename = f'{MEDIA_ROOT}/pdf/{check_data["order"]["order_number"]}_{check_data["type"]}.html'
    with open(html_filename, 'w') as f:
        f.write(html_content)

    data = {
        'contents': """
        <!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Check</title>
</head>
<body>
{{ data }}
</body>
</html>""",
        'options': {
            'margin-top': '6',
            'margin-left': '6',
            'margin-right': '6',
            'margin-bottom': '6',
            'page-width': '105mm',
            'page-height': '40mm'
        }
    }

    response = requests.post(URL, data=json.dumps(data, ensure_ascii=True), headers=HEADERS)
    print(
        'Data         ',json.dumps(data, ensure_ascii=True),
    )
    print(
        'html_content dumps   ',json.dumps(html_content, ensure_ascii=True),
        sep='\n'
    )
    if response.status_code == 200:
        pdf_filename = f'{MEDIA_ROOT}/pdf/{check_data["order"]["order_number"]}_{check_data["type"]}.pdf'
        with open(pdf_filename, 'wb') as f:
            f.write(response.content)
    else:
        print(f"Error generating PDF: {response.status_code} - {response.text}")

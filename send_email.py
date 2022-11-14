# using SendGrid's Python Library
# https://github.com/sendgrid/sendgrid-python
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

message = Mail(
    from_email='enrique.sobrados@utec.edu.pe',
    to_emails='cesar.madera@utec.edu.pe',
    subject='Test Proyecto IOT',
    html_content='<strong> Te están robando la hato, aiuda </strong>')
try:
    sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
    response = sg.send(message)
    print(response.status_code)
    print(response.body)
    print(response.headers)
except Exception as e:
    print(e)
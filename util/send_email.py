# using SendGrid's Python Library
# https://github.com/sendgrid/sendgrid-python
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from datetime import datetime

from dotenv import dotenv_values
sengrid_file = "sendgrid.env"
config = dotenv_values(sengrid_file) 

message = Mail(
    from_email='johan.tanta@utec.edu.pe',
    to_emails='johantv15@gmail.com',
    subject='NOTIFICACIÓN DE ALARMA',
    html_content='<strong> Se ha detectado un posible intruso a las ' + str(datetime.now()) + '</strong>')
try:
    sg = SendGridAPIClient(config['SENDGRID_API_KEY'])
    response = sg.send(message)
    print(response.status_code)
    print(response.body)
    print(response.headers)
except Exception as e:
    print(e)
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from datetime import datetime

def send_message(api_key):
    message = Mail(
        from_email='johan.tanta@utec.edu.pe',
        to_emails='johantv15@gmail.com',
        subject='NOTIFICACION DE ALARMA',
        html_content='<strong> Se ha detectado un posible intruso a las ' + str(datetime.now()) + '</strong>')
    
    try:
        sg = SendGridAPIClient(api_key)
        sg.send(message)
        print("Se envio notificación de alarma - via electronico")
    except Exception as e:
        print(e)
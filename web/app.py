from flask import Flask
from flask import render_template
from flask import request
import re
import random
from paho.mqtt import client as mqtt_client
import pandas as pd
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

broker = '192.168.148.238'
port = 10000
topic = "test/topic"
# generate client ID with pub prefix randomly
client_id = f'python-mqtt-{random.randint(0, 100)}'
username = ''
password = ''
user_email = 'camgcamg11@gmail.com'

message = Mail(
    from_email='johan.tanta@utec.edu.pe',
    to_emails='cesar.madera@utec.edu.pe',
    subject='Test Proyecto IOT',
    html_content='<strong> Te están robando la hato, aiuda </strong>')
from dotenv import load_dotenv

load_dotenv()

def send_message():
    try:
        sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        print(os.environ.get('SENDGRID_API_KEY'))
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(e)

def connect_mqtt() -> mqtt_client:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            #print("Connected to MQTT Broker!")
            next
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    #client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client

def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        message_decoded = msg.payload.decode()
        print(message_decoded)
        splitted_message = message_decoded.split()
        if splitted_message[0] == "connect":
            with open('./data.csv','a') as f:
                f.write(f'{splitted_message[1]}\n')
        elif splitted_message[0] == "alarma":
            send_message()
        #print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")


    client.subscribe(topic)
    client.on_message = on_message

client = connect_mqtt()
subscribe(client)
client.loop_start()
app = Flask(__name__)

def get_devices():
    df = pd.read_csv('./data.csv')
    conected_devices = df['ID'].tolist()
    return conected_devices


def validate_strings(tiempo,distancia,topic,email):
    
    # Verify time string
    time_regex = r"^[0-9]+$"
    if not re.fullmatch(time_regex, tiempo):
        return False
    elif 5 > int(tiempo) > 200: 
        return False

    # Verify email string
    email_regex = r"^\S+@\S+\.\S+$"
    if not re.fullmatch(email_regex, email):
        return False

    # Verify distance String 
    distance_regex = r"^[0-9]+$"
    if not re.fullmatch(distance_regex, distancia):
        return False
    elif 5 > int(distancia) > 200: 
        return False

    topic_regex = r"^\w+/*\w+$"
    if not re.fullmatch(topic_regex, topic) or len(topic) > 30:
        return False
    return True 

def create_file():
    os.remove("./data.csv")
    with open("./data.csv", "w") as f:
        f.write('ID\n')
        f.close()


def publish(devices,variable,value):
    global client
    for device in devices:
        client.publish(topic,f'{device}|{variable}|{value}')
        
@app.route('/')
def default():
    return render_template('index.html')

@app.route('/index')
def index(name=None):
    return render_template('index.html', name=name)



@app.route('/set_parameters')
def set_parameters():
    tiempo = request.args.get('tiempo')
    distancia = request.args.get('distancia')
    topic = request.args.get('topic')
    email = request.args.get('correo')
    devices = get_devices()
    print(devices)
    if (tiempo!=""):
        publish(devices,"timeThreshold",tiempo)
    if (distancia!=""):
        publish(devices,"distanceThreshold",distancia)
    if (email!=""):
        user_email = email

    print(tiempo)
    print(distancia)
    print(topic)
    print(email)


    if validate_strings(tiempo,distancia,topic,email):
        return "<p> Successful </p>"
    return "<p> Not valid parameters </p>"

if __name__ == '__main__':
    create_file() 
    app.run(host='localhost', port=8080)

from flask import Flask
from flask import render_template
from flask import request
import re
import pandas as pd
import os

from constants.constants import SENDGRID_API_KEY, BROKER, PORT
from services.send_email import send_message
from services.mqtt import connect_mqtt

topic = "test/topic"
# generate client ID with pub prefix randomly


app = Flask(__name__)
mqtt_client = None

def subscribe(client, topic):
    def on_message(client, userdata, msg):
        message_decoded = msg.payload.decode()
        print(message_decoded)
        splitted_message = message_decoded.split()
        
        if splitted_message[0] == "connect":
            with open('./data.csv','a') as f:
                f.write(f'{splitted_message[1]}\n')
        elif splitted_message[0] == "alarma":
            send_message(SENDGRID_API_KEY)
        #print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")

    client.subscribe(topic)
    client.on_message = on_message
    

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
    if os.path.exists('./data.csv'):
        os.remove("./data.csv")
    
    with open("./data.csv", "w") as f:
        f.write('ID\n')
        f.close()


def publish(devices,variable,value):
    global mqtt_client
    for device in devices:
        mqtt_client.publish(topic,f'{device}|{variable}|{value}')
        
@app.route('/')
def default():
    return render_template('index.html')

@app.route('/index')
def index(name=None):
    return render_template('index.html', name=name)

@app.route('/send_email')
def send():
    send_message(SENDGRID_API_KEY)
    return "<p>Email enviado</p>"

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
    mqtt_client = connect_mqtt(BROKER, PORT)
    subscribe(mqtt_client, topic)
    mqtt_client.loop_start()
    
    create_file()
    app.run(host="0.0.0.0", port=8080, threaded=True)
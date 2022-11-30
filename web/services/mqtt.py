from paho.mqtt import client as mqtt_client
import random

def connect_mqtt(broker, port, client_id = f'python-mqtt-{random.randint(0, 100)}') -> mqtt_client:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            #print("Connected to MQTT Broker!")
            next
        else:
            print("Failed to connect, return code %d\n", rc)

    client_ = mqtt_client.Client(client_id)
    #client.username_pw_set(USERNAME, PASSWORD)
    client_.on_connect = on_connect
    client_.connect(broker, port)
    return client_
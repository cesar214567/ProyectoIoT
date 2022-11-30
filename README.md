# ProyectoIoT


## Initialize Broker

chmod +x broker_mqtt/run.sh <br> 
./broker_mqtt/run.sh

## Before running app.py

echo "export SENDGRID\_API\_KEY='SG.XXX....XXXX'" > env.env <br> 
echo "env.env" >> .gitignore (SKIP THIS) <br> 
source ./env.env

## Execute Arduino

Use ESP8266WiFi module with this implementation.

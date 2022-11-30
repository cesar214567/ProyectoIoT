# ProyectoIoT


## Initialize Broker

chmod +x broker_mqtt/run.sh <br> 
./broker_mqtt/run.sh

## Before running app.py

echo "export SENDGRID\_API\_KEY='SG.XXX....XXXX'" > sendgrid.env <br> 
echo "sendgrid.env" >> .gitignore (SKIP THIS) <br> 
source ./sendgrid.env

## Execute Arduino

Use ESP8266WiFi module with this implementation.

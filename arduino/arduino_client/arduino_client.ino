#include <ESP8266WiFi.h>
#include <PubSubClient.h>// WiFi
#include <ezButton.h>

const int Trigger = 12;// connecting to port 12, in board is D6
const int Echo = 14;  // connecting to port 14, in board is D5
const int LED = 16; //connecting to port 16, in board is D0
const int Button = 5; //connecting to port 5, in board is D1, the other one goes in ground 
ezButton toggleSwitch(Button);


bool button_switch = false;
const char *ssid = "JohanTv"; // Enter your WiFi name
const char *password = "123456789"; // Enter WiFi password// MQTT Broker
const char *mqtt_broker = "192.168.26.244"; // Enter your WiFi or Ethernet IP
const char *topic = "test/topic";   //Enter topic 
const int mqtt_port = 10000;      //Enter MQTT port
double distanceThreshold = 50;
double timeThreshold = 15000; //milliseconds
bool thiefDetected = false;
long int lastRecord = 0;
bool alarm_sent = false;

WiFiClient espClient;
PubSubClient client(espClient);

//define sound velocity in cm/uS

double duration;
double distanceCm;
double prevDistance;
String client_id = "esp8266-client-";

char buff[10];
void setup() {
  // Set software serial baud to 115200;
  pinMode(Trigger, OUTPUT); // Sets the trigPin as an Output
  pinMode(Echo, INPUT); // Sets the echoPin as an Input
  pinMode(LED_BUILTIN, OUTPUT);

  Serial.begin(115200);
  
  // connecting to a WiFi network
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.println("Connecting to WiFi..");
  }
  Serial.println("Connected to the WiFi network");
  
  //connecting to a mqtt broker
  client.setServer(mqtt_broker, mqtt_port);
  client.setCallback(callback);
  client_id += String(WiFi.macAddress());
  while (!client.connected()) {
    Serial.printf("The client %s connects to mosquitto mqttbroker\n", client_id.c_str());
    if (client.connect(client_id.c_str())) {
      Serial.println("Public emqx mqtt broker connected");
    } else {
      Serial.print("failed with state ");
      Serial.print(client.state());
      delay(2000);
    }
  }
  prevDistance = 0.0;
  // publish and subscribe
  String connect_message = "connect " + client_id;
  client.publish(topic, connect_message.c_str());
  client.subscribe(topic);
}

//Setting callback when someone publish anything to the topic
void callback(char *topic, byte *payload, unsigned int length) {
  
  if (length >= client_id.length()){
    int length_obtained = 0;
    char *token = strtok((char*)payload, "|");
    double *pointer = NULL;
     /* walk through other tokens */
     if( strcmp(client_id.c_str(),token)==0){
      length_obtained += String(token).length();
       while( length_obtained < length ) {
          token = strtok(NULL, "|");
          length_obtained += String(token).length();
          if(strcmp(token,"distanceThreshold")==0){
            pointer = &distanceThreshold;
            Serial.println("distanceThreshold: ");
          }else if (strcmp(token,"timeThreshold")==0){ 
            pointer = &timeThreshold;
            Serial.println("timeThreshold: ");
          }else{
            *pointer = String(token).toFloat();
            Serial.println(*pointer);
          }
       } 
     }else{
      return;
     }

  }
}

bool motionDetected(){
  return distanceCm  < distanceThreshold;
}

bool timeThresholdPassed(){
  return millis() - lastRecord > timeThreshold;
}


void loop() {
    toggleSwitch.loop();
    client.loop();
    if (toggleSwitch.isReleased()){
      Serial.println("button_pressed");
      button_switch = !button_switch;
    }
    if (button_switch){
      delay(3000);
      return;
    }
    digitalWrite(Trigger, LOW);
    delayMicroseconds(4);
    // Sets the trigPin on HIGH state for 10 micro seconds
    digitalWrite(Trigger, HIGH);
    delayMicroseconds(10);
    digitalWrite(Trigger, LOW);
    
    // Reads the echoPin, returns the sound wave travel time in microseconds
    duration = pulseIn(Echo, HIGH);
    
    // Calculate the distance
    distanceCm = duration/58.4;

    if (motionDetected()){ 
      if (!thiefDetected){
        lastRecord = millis();
      }
      thiefDetected = true;
      if(timeThresholdPassed() && !alarm_sent){
        //alarma
        Serial.println("alarma");
        client.publish(topic,"alarma");
        alarm_sent = true;

        digitalWrite(LED, HIGH);   // turn the LED on (HIGH is the voltage level)

      }
    }else{
      thiefDetected = false;  
      alarm_sent = false;
    }
    
    client.publish(topic,String(distanceCm,4).c_str());

    // Prints the distance on the Serial Monitor
    Serial.println(distanceCm);
    
    prevDistance = distanceCm;
    delay(3000);
    
    digitalWrite(LED, LOW);   // turn the LED on (HIGH is the voltage level)

}

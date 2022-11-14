#include <ESP8266WiFi.h>
#include <PubSubClient.h>// WiFi
const int Trigger = 12;// connecting to port 12, in board is D6
const int Echo = 14;  // connecting to port 14, in board is D5
const int LED = 16; //connecting to port 16, in board is D0
const char *ssid = "Galaxy A121A09"; // Enter your WiFi name
const char *password = "yynm5492"; // Enter WiFi password// MQTT Broker
const char *mqtt_broker = "192.168.148.238"; // Enter your WiFi or Ethernet IP
const char *topic = "test/topic";   //Enter topic 
const int mqtt_port = 10000;      //Enter MQTT port
const double distanceThreshold = 50;
const double timeThreshold = 15000; //milliseconds
bool thiefDetected = false;
long int lastRecord = 0;
WiFiClient espClient;
PubSubClient client(espClient);

//define sound velocity in cm/uS

double duration;
double distanceCm;
double prevDistance;
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
  while (!client.connected()) {
    String client_id = "esp8266-client-";
    client_id += String(WiFi.macAddress());
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
  client.publish(topic, "Hello From ESP8266!");
  client.subscribe(topic);
}

//Setting callback when someone publish anything to the topic
void callback(char *topic, byte *payload, unsigned int length) {
  Serial.print("Message arrived in topic: ");
  Serial.println(topic);
  Serial.print("Message:");
  for (int i = 0; i < length; i++) {
    Serial.print((char) payload[i]);
  }
  Serial.println();
  Serial.println(" - - - - - - - - - - - -");
}

bool motionDetected(){
  return distanceCm  < distanceThreshold;
}

bool timeThresholdPassed(){
  return millis() - lastRecord > timeThreshold;
}


void loop() {
  client.loop();
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
      if(timeThresholdPassed()){
        //alarma
        Serial.println("jaja se mamo");
        digitalWrite(LED, HIGH);   // turn the LED on (HIGH is the voltage level)

      }
    }else{
      thiefDetected = false;  
    }
    

    // Prints the distance on the Serial Monitor
    //client.publish(topic,"Duration (?): ");
    //client.publish(topic,String(duration).c_str());
    
    //client.publish(topic,"Distance (cm): ");
    client.publish(topic,String(distanceCm,4).c_str());
    Serial.println(distanceCm);
    prevDistance = distanceCm;
    delay(3000);
    
    digitalWrite(LED, LOW);   // turn the LED on (HIGH is the voltage level)

}

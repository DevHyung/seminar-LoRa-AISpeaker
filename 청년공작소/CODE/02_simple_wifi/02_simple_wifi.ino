#include <ESP8266WiFi.h>
#include <WiFiClient.h>
#include <ESP8266WebServer.h>
#include <ESP8266mDNS.h>

const char* ssid = "홍춘투지";
const char* password = "01041398117";

ESP8266WebServer server(80);

const int LED_PIN = 14;

String s = "<!DOCTYPE html><html><head><meta name=\"viewport\" content=\"width=device-width, user-scalable=no\"></head><body><br><input type=\"button\" name=\"b1\" value=\"ON\" onclick=\"location.href='/on'\" style=\"width:100%;height:70px;font-weight:bold;font-size:1em\"><br/><input type=\"button\" name=\"b1\" value=\"OFF\" onclick=\"location.href='/off'\" style=\"width:100%;height:80px;font-weight:bold;font-size:1em\"></body></html>";


void handleRoot() {
  //digitalWrite(led, 1);
  server.send(200, "text/html", s);
  //digitalWrite(led, 0);
}

void handleNotFound(){
  //digitalWrite(led, 1);
  String message = "File Not Found\n\n";
  message += "URI: ";
  message += server.uri();
  message += "\nMethod: ";
  message += (server.method() == HTTP_GET)?"GET":"POST";
  message += "\nArguments: ";
  message += server.args();
  message += "\n";
  for (uint8_t i=0; i<server.args(); i++){
    message += " " + server.argName(i) + ": " + server.arg(i) + "\n";
  }
  server.send(404, "text/html", message);
  //digitalWrite(led, 0);
}

void setup(void){
  //pinMode(led, OUTPUT);
  //digitalWrite(led, 0);
  Serial.begin(115200);
  WiFi.begin(ssid, password);
  Serial.println("");

  // Wait for connection
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.print("Connected to ");
  Serial.println(ssid);
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());

  if (MDNS.begin("esp8266")) {
    Serial.println("MDNS responder started");
  }

  server.on("/", handleRoot);

  //on
  server.on("/on", [](){    
    digitalWrite(LED_PIN, HIGH);
    Serial.println("POWER ON");
    server.send(200, "text/html", s);
  });

  //off
  server.on("/off", [](){
    digitalWrite(LED_PIN, LOW);
    Serial.println("POWER OFF");
    server.send(200, "text/html", s);
  });

  server.onNotFound(handleNotFound);

  server.begin();
  Serial.println("HTTP server started");

  pinMode(LED_PIN, OUTPUT); //GPIO14 is an OUTPUT pin;
  digitalWrite(LED_PIN, HIGH); //Initial state is OFF

}

void loop(void){
  server.handleClient();  
}

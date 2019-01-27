/*
    This sketch sends data via HTTP GET requests to data.sparkfun.com service.

    You need to get streamId and privateKey at data.sparkfun.com and paste them
    below. Or just customize this script to talk to other HTTP servers.

*/
#include <SoftwareSerial.h>
#include <ESP8266WiFi.h>
#include <WiFiClient.h>
#include <ESP8266WebServer.h>
#include <ESP8266mDNS.h>
#include "SNIPE.h" 

#define ATSerial Serial

String lora_app_key = "11 22 33 44 55 66 77 88 99 aa bb cc dd ee ff 11";  //16byte hex key, Last number matching to ADDR

const char* ssid     = "SSID";
const char* password = "PW";
#define ADDR  0x11
#define NODE1_ON  1
#define NODE1_OFF  2
ESP8266WebServer server ( 80 );

#define TXpin D9
#define RXpin D8
SoftwareSerial DebugSerial(RXpin,TXpin);
SNIPE SNIPE(ATSerial);

WiFiClient client;
String s = "<!DOCTYPE html><html><head><meta name=\"viewport\" content=\"width=device-width, user-scalable=no\"></head><body><br><input type=\"button\" name=\"b1\" value=\"ON\" onclick=\"location.href='/on'\" style=\"width:100%;height:70px;font-weight:bold;font-size:1em\"><br/><input type=\"button\" name=\"b1\" value=\"OFF\" onclick=\"location.href='/off'\" style=\"width:100%;height:80px;font-weight:bold;font-size:1em\"></body></html>";
int addr;
int mode;
int sendResult;
String packet;
String ver;
int count;
char buffer[20];

void setup() {
  ATSerial.begin(115200);
  // put your setup code here, to run once:
  while(ATSerial.read()>= 0) {}
  while(!ATSerial);

  DebugSerial.begin(115200);

  if (!SNIPE.lora_init()) {
    DebugSerial.println("SNIPE LoRa Initialization Fail!");
    while (1);
  }  

  /* SNIPE LoRa Set AppKey */
  if (!SNIPE.lora_setAppKey(lora_app_key)) {
    DebugSerial.println("SNIPE LoRa app key value has not been changed");
  }

  /* SNIPE LoRa Set Frequency */
  if (!SNIPE.lora_setFreq(LORA_CH_2)) {
    DebugSerial.println("SNIPE LoRa Frequency value has not been changed");
  }

  /* SNIPE LoRa Set Spreading Factor */
  if (!SNIPE.lora_setSf(LORA_SF_7)) {
    DebugSerial.println("SNIPE LoRa Sf value has not been changed");
  }

  /* SNIPE LoRa Set Rx Timeout */
  if (!SNIPE.lora_setRxtout(2000)) {
    DebugSerial.println("SNIPE LoRa Rx Timout value has not been changed");
  }    
    
  DebugSerial.println("Simple LoRa Gateway StartUP");

  // We start by connecting to a WiFi network

  DebugSerial.println();
  DebugSerial.println();
  DebugSerial.print("Connecting to ");
  DebugSerial.println(ssid);

  // WIFI Add
  WiFi.begin ( ssid, password );
  // Wait for connection
  while ( WiFi.status() != WL_CONNECTED ) {
    delay ( 500 );
    DebugSerial.print ( "." );
  }

  DebugSerial.println ( "" );
  DebugSerial.print ( "Connected to " );
  DebugSerial.println ( ssid );
  DebugSerial.print ( "IP address: " );
  DebugSerial.println ( WiFi.localIP() );

//  Serial.println ( "" );
//  Serial.print ( "Connected to " );
//  Serial.println ( ssid );
//  Serial.print ( "IP address: " );
//  Serial.println ( WiFi.localIP() );
  if ( MDNS.begin ( "esp8266" ) ) {
    DebugSerial.println ( "MDNS responder started" );
  }

  
  server.on ( "/", handleRoot );
  server.on ( "/on", onFunction );
  server.on ( "/off", offFunction );
  
  server.onNotFound ( handleNotFound );
  server.begin();
  DebugSerial.println ( "HTTP server started" );
}

void loop() {
  server.handleClient();
}
void onFunction(){
  addr = ADDR;
  mode = NODE1_ON;
  count = 10;
  memset(buffer, 0x0, sizeof(buffer));

  sprintf(buffer, "%d:%d", addr, mode);
  packet = (String)buffer;
  DebugSerial.println(packet);

  /* send Packet */
  do{
    delay(100);
    sendResult = SNIPE.lora_send(packet);
    DebugSerial.println(sendResult);
  }while(!sendResult);

  while(count)
  {
    /* result Packet */
    ver = SNIPE.lora_recv();
    DebugSerial.println(ver);
    if (ver != "AT_RX_TIMEOUT" && ver != "AT_RX_ERROR")
    {
      DebugSerial.println(ver);
      memset(buffer, 0x0, sizeof(buffer));
      ver.toCharArray(buffer, sizeof(buffer));
      sscanf(buffer, "%d:%d", &addr, &mode);
      
      if(addr == ADDR)
      {
        break;
      }
    }
    else
    {
      count--;
    }
  }
  server.send ( 200, "text/html", s);
}

void offFunction(){
  addr = ADDR;
  mode = NODE1_OFF;
  count = 10;
  memset(buffer, 0x0, sizeof(buffer));

  sprintf(buffer, "%d:%d", addr, mode);
  packet = (String)buffer;
  DebugSerial.println(packet);

  /* send Packet */
  do{
    delay(100);
    sendResult = SNIPE.lora_send(packet);
    DebugSerial.println(sendResult);
  }while(!sendResult);

  while(count)
  {
    /* result Packet */
    ver = SNIPE.lora_recv();
    DebugSerial.println(ver);
    if (ver != "AT_RX_TIMEOUT" && ver != "AT_RX_ERROR")
    {
      DebugSerial.println(ver);
      memset(buffer, 0x0, sizeof(buffer));
      ver.toCharArray(buffer, sizeof(buffer));
      sscanf(buffer, "%d:%d", &addr, &mode);
      
      if(addr == ADDR)
      {
        break;
      }
    }
    else
    {
      count--;
    }
  }
  server.send ( 200, "text/html", s);
}

void handleRoot() {
  server.send(200, "text/html", s);
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

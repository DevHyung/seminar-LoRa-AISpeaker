/*
 *  HTTP over TLS (HTTPS) example sketch
 *
 *  This example demonstrates how to use
 *  WiFiClientSecure class to access HTTPS API.
 *  We fetch and display the status of
 *  esp8266/Arduino project continuous integration
 *  build.
 *
 *  Created by Ivan Grokhotkov, 2015.
 *  This example is in public domain.
 */

/*
꼭꼭꼭 !!!
64번줄 수정해주셔야합니다 !!!
*/
#include <ESP8266WiFi.h>
#include <WiFiClientSecure.h>
const char* ssid     = "홍춘투지";
const char* password = "01041398117";

void setup() {
  WiFi.persistent(false);
  Serial.begin(115200);
  Serial.println();
  Serial.print("connecting to ");
  Serial.println(ssid);
  //delay(10);
  WiFi.begin(ssid, password);
  //delay(10);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
}

void loop() {
}

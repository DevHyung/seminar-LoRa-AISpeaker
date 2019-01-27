#include <Servo.h> //Servo 라이브러리 추가
#include <SoftwareSerial.h>
#include "SNIPE.h"  //SNIPE 라이브러리 추가

#define TXpin 11
#define RXpin 10
#define ATSerial Serial

Servo servo;      //Servo 클래스로 servo객체 생성
String lora_app_key = "11 22 33 44 55 66 77 88 99 aa bb cc dd ee ff 11";  //16byte hex key, Last number matching to ADDR

SoftwareSerial DebugSerial(RXpin,TXpin);
SNIPE SNIPE(ATSerial);

/*  Packet Structure 
 *  (ADDR):(NODE_ON or NODE_OFF)
*/
#define ADDR  0x11
#define NODE_ON   1 
#define NODE_OFF  2

int addr;
int mode;
int sendResult;

char buffer[20];

void onFunction(){
  int angle;
  
  for(angle = 0; angle < 30; angle++) 
  {
    servo.write(angle); 
    delay(4);
  }     
}

void offFunction(){
  int angle;
  
  for(angle = 30; angle > 0; angle--) 
  {
    servo.write(angle); 
    delay(4); 
  } 
}

void setup() {
  servo.attach(7);     //맴버함수인 attach : 핀 설정
  servo.write(0);
  ATSerial.begin(115200);
  pinMode(LED_BUILTIN, OUTPUT);
  digitalWrite(LED_BUILTIN, HIGH);
  // put your setup code here, to run once:
  while(ATSerial.read()>= 0) {}
  while(!ATSerial);

  DebugSerial.begin(115200);

  /* SNIPE LoRa Initialization */
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
  DebugSerial.println("LoRa AI Switch Test");
  
  digitalWrite(LED_BUILTIN, LOW);
}

void loop() {
  String ver = SNIPE.lora_recv();
  DebugSerial.println(ver);

  if (ver != "AT_RX_TIMEOUT" && ver != "AT_RX_ERROR")
  {
    DebugSerial.println(ver);

    memset(buffer, 0x0, sizeof(buffer));
    ver.toCharArray(buffer, sizeof(buffer));
    sscanf(buffer, "%d:%d", &addr, &mode);
    DebugSerial.println(addr);

    if(addr == ADDR)
    {
      if(mode == NODE_ON){
        onFunction();
      }else if(mode == NODE_OFF){
        offFunction();
      }
      
      DebugSerial.println(SNIPE.lora_getRssi());
      DebugSerial.println(SNIPE.lora_getSnr());

      /* result ACK */
      memset(buffer, 0x0, sizeof(buffer));
      sprintf(buffer, "%d:%d", addr, mode);

      ver = (String)buffer;
      do{
         delay(100); 
         sendResult = SNIPE.lora_send(ver);
      }while(!sendResult);
      
      DebugSerial.println("send ack complete");
    }
    else
    {
      DebugSerial.println("It is not my address!!!");
    }      
  }
}

#include <SoftwareSerial.h>
#include "SNIPE.h"

#define TXpin 11
#define RXpin 10
#define ATSerial Serial

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

  addr = ADDR;
  mode = NODE_ON;
  DebugSerial.println("LoRa AI Switch Test");
}

void loop() {
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
        if(mode == NODE_ON)
          mode = NODE_OFF;
        else if(mode == NODE_OFF)
          mode = NODE_ON;
        break;
      }
    }
    else
    {
      count--;
    }
  }
  delay(3000);
}

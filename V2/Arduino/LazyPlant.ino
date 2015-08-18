#include <Wire.h>//声明I2C库文件
#include "RTClib.h"
#include <Adafruit_NeoPixel.h>
#ifdef __AVR__
  #include <avr/power.h>
#endif
#include <Servo.h>

Servo myservo;

#define PROTO_START 53
#define PROTO_END 55

#define CMD_RTC 10
#define CMD_TEMPERATURE 11
#define CMD_HUMIDITY 12
#define CMD_MOISTURE 13
#define CMD_THERMAL 14
#define CMD_WATER_LEVEL 15
#define CMD_ILLUMINATION 16
#define CMD_PUMP 17
#define CMD_PERISTALTIL 18
#define CMD_LED 19
#define CMD_CAM 20
#define CMD_ROTATE 21
#define CMD_FAN 22
#define CMD_HUMIDITY_UP 23
#define CMD_HEAT_UP 24

RTC_DS1307 RTC;
#define LED_PIN            6
#define LED_NUMPIXELS      16

int Control_LED_State = 0;

Adafruit_NeoPixel led_pixels = Adafruit_NeoPixel(LED_NUMPIXELS, LED_PIN, NEO_GRB + NEO_KHZ800);
int delayval = 500; // delay for half a second

unsigned char g_Req_Command = 0;
unsigned char g_Req_Para = 0;
unsigned char g_Req_Start = 0;
unsigned char g_Req_End = 0;
char g_ReceiveDat[16];
unsigned char g_ReceiveLen = 0;
unsigned char end_flag;

unsigned int g_value_temperature = 10;
unsigned int g_value_humidity = 20;
unsigned int g_value_moisture = 30;
unsigned int g_value_thermal = 40;
unsigned int g_value_water_up = 50;
unsigned int g_value_water_down = 60;
unsigned int g_value_illumination = 70;

//初始化
void setup()
{
#if defined (__AVR_ATtiny85__)
  if (F_CPU == 16000000) clock_prescale_set(clock_div_1);
#endif
  led_pixels.begin(); // This initializes the NeoPixel library.
  RTC.begin();  
  ///RTC.adjust(DateTime(15, 8, 12, 17, 34 , 0));
    
  Wire.begin(4);                // 加入 i2c 总线，设置从机地址为 #4
  Wire.onReceive(receiveEvent); //注册接收到主机字符的事件
  Wire.onRequest(requestEvent); // 注册主机通知从机上传数据的事件
  
  myservo.attach(9);
  
  pinMode(8, OUTPUT);
  pinMode(10, OUTPUT);
  pinMode(11, OUTPUT);
  pinMode(12, OUTPUT);
  pinMode(13, OUTPUT);
  
  Serial.begin(9600);           //设置串口波特率
  Serial.println("start");
}
//主程序
void loop()
{
  delay(500);//延时
  
  if(Control_LED_State==0)
  {
    for(int i=0;i<LED_NUMPIXELS;i++){
      led_pixels.setPixelColor(i, led_pixels.Color(0,0,0)); // Moderately bright green color.
    }
    led_pixels.show(); // This sends the updated pixel color to the hardware.     
  }
  
  DateTime now = RTC.now();
    
  if(g_Req_Command==CMD_RTC)
  {
    Serial.println("RTC");
    
    Serial.print(now.year(), DEC);
    Serial.print('/');
    Serial.print(now.month(), DEC);
    Serial.print('/');
    Serial.print(now.day(), DEC);
    Serial.print(' ');
    Serial.print(now.hour(), DEC);
    Serial.print(':');
    Serial.print(now.minute(), DEC);
    Serial.print(':');
    Serial.print(now.second(), DEC);
    Serial.println();
    
    g_Req_Command = 0;
  }
  else if(g_Req_Command==CMD_PUMP)
  {
    Serial.println("PUMP");
    if(g_Req_Para==0)
    {
      digitalWrite(8, HIGH);
    }    
    else
    {
      digitalWrite(8, LOW);
    }
  
    g_Req_Command = 0;
  }
  else if(g_Req_Command==CMD_PERISTALTIL)
  {
    Serial.println("PERISTALTIL");

    if(g_Req_Para==1)
    {
      digitalWrite(10, HIGH);
    }
    else
    {
      digitalWrite(10, LOW);
    }
    
    g_Req_Command = 0;
  }
  else if(g_Req_Command==CMD_LED)
  {
    if(g_Req_Para==1)
    {
      for(int i=0;i<LED_NUMPIXELS;i++){
        led_pixels.setPixelColor(i, led_pixels.Color(150,150,150)); // Moderately bright green color.
      }
      led_pixels.show(); // This sends the updated pixel color to the hardware. 
      
      Control_LED_State = 1;
    }
    else
    {
      for(int i=0;i<LED_NUMPIXELS;i++){
        led_pixels.setPixelColor(i, led_pixels.Color(0,0,0)); // Moderately bright green color.
      }
      led_pixels.show(); // This sends the updated pixel color to the hardware. 
      
      Control_LED_State = 0;
    }

    g_Req_Command = 0;
  }
  else if(g_Req_Command==CMD_CAM)
  {
    Serial.println("CAMERA");
    g_Req_Command = 0;
  }  
  else if(g_Req_Command==CMD_ROTATE)
  {
    if(g_Req_Para==0)
    {    
      Serial.println("ROTATE 0");
      myservo.write(0); 
    }
    else if(g_Req_Para==1)
    {    
      Serial.println("ROTATE 90");
      myservo.write(90); 
    }
    else if(g_Req_Para==2)
    {    
      Serial.println("ROTATE 180");
      myservo.write(180); 
    }
    g_Req_Command = 0;
  }  
  else if(g_Req_Command==CMD_FAN)
  {
    Serial.println("FAN");
    if(g_Req_Para==1)
    {
      digitalWrite(13, HIGH);
    }  
    else
    {
      digitalWrite(13, LOW);
    }

    g_Req_Command = 0;
  }  
  else if(g_Req_Command==CMD_HUMIDITY_UP)
  {
    Serial.println("HUMIDITY UP");
    if(g_Req_Para==1)
    {
      digitalWrite(11, HIGH);
    }   
    else
    {
      digitalWrite(11, LOW);
    }

    
    g_Req_Command = 0;
  }
  else if(g_Req_Command==CMD_HEAT_UP)
  {
    Serial.println("HEAT UP");
    g_Req_Command = 0;
    if(g_Req_Para==1)
    {
      digitalWrite(12, HIGH);
    }  
    else
    {
      digitalWrite(12, LOW);
    }
  }    

}

// 当从机接收到主机字符，执行该事件
void receiveEvent(int howMany)
{
  while ( Wire.available() > 1) // 循环执行，直到数据包只剩下最后一个字符
  {
    g_ReceiveDat[g_ReceiveLen] = Wire.read(); // 作为字符接收字节
    Serial.print(g_ReceiveDat[g_ReceiveLen]);

    g_ReceiveLen++;
  }
  
  //接收主机发送的数据包中的最后一个字节
  end_flag = Wire.read();
  Serial.print(end_flag);
  
  Serial.println("GET"); 
  
  if(g_ReceiveLen>3 && end_flag>50)
  {
    g_Req_Command = g_ReceiveDat[1];
    g_Req_Para = g_ReceiveDat[2];
    g_Req_Start = g_ReceiveDat[3];
    g_Req_End = g_ReceiveDat[4];
    Serial.println(g_Req_Command);
    Serial.println(g_Req_Para);
    Serial.println(g_Req_Start);
    Serial.println(g_Req_End);
  }
  
  g_ReceiveLen = 0;
}

//当主机通知从机上传数据，执行该事件
void requestEvent()
{

  if(g_Req_Command==CMD_TEMPERATURE)
  {
    Wire.write( g_value_temperature>>8&0xFF);
    Wire.write( g_value_temperature&0xFF);
  }
  else if(g_Req_Command==CMD_HUMIDITY)
  {
    Wire.write( g_value_humidity>>8&0xFF);
    Wire.write( g_value_humidity&0xFF);
  }
  else if(g_Req_Command==CMD_MOISTURE)
  {
    Wire.write( g_value_moisture>>8&0xFF);
    Wire.write( g_value_moisture&0xFF);
  }
  else if(g_Req_Command==CMD_THERMAL)
  {
    Wire.write( g_value_thermal>>8&0xFF);
    Wire.write( g_value_thermal&0xFF);
  }
  else if(g_Req_Command==CMD_WATER_LEVEL)
  {
    Wire.write( g_value_water_up>>8&0xFF);
    Wire.write( g_value_water_up&0xFF);
  }
  else if(g_Req_Command==CMD_ILLUMINATION)
  {
    Wire.write( g_value_illumination>>8&0xFF);
    Wire.write( g_value_illumination&0xFF);
  }
}

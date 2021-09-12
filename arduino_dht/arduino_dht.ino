//Libraries
#include <DHT.h>

//Constants
#define DHTPIN 7     // what pin we're connected to
#define DHTTYPE DHT22   // DHT 22  (AM2302)
DHT dht(DHTPIN, DHTTYPE); //// Initialize DHT sensor for normal 16mhz Arduino
char in_char;

void setup()
{
  pinMode(LED_BUILTIN, OUTPUT);
  Serial.begin(9600);
  dht.begin();
}

void loop()
{

}

void serialEvent()
{
  in_char = Serial.read();
  digitalWrite(LED_BUILTIN, HIGH);
  if (in_char == 'h')
  {
    digitalWrite(LED_BUILTIN, HIGH);
    Serial.println(dht.readHumidity());
  }else if(in_char == 't')
  {
    Serial.println(dht.readTemperature());
  }
}

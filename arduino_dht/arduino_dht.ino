//Libraries
#include <DHT.h>

#include <Wire.h>
#include <SPI.h>
#include <Adafruit_BMP280.h>

#define BMP_SCK  (13)
#define BMP_MISO (12)
#define BMP_MOSI (11)
#define BMP_CS   (10)
Adafruit_BMP280 bmp; // I2C
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
  bmp.begin();
  bmp.setSampling(Adafruit_BMP280::MODE_NORMAL,     /* Operating Mode. */
                  Adafruit_BMP280::SAMPLING_X2,     /* Temp. oversampling */
                  Adafruit_BMP280::SAMPLING_X16,    /* Pressure oversampling */
                  Adafruit_BMP280::FILTER_X16,      /* Filtering. */
                  Adafruit_BMP280::STANDBY_MS_500); /* Standby time. */
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
    Serial.println(dht.readHumidity());
  }else if(in_char == 't')
  {
    Serial.println(dht.readTemperature());
  }else if(in_char == 'p')
  {
    Serial.println(bmp.readPressure());
  }else if(in_char == 'k')
  {
    Serial.println(bmp.readTemperature());
  }
}

#include <WiFi.h>

void setup(){
  Serial.begin(115200);
  WiFi.mode(WIFI_STA);
  Serial.print("ESP32 MAC Address: ");
  delay(1000); // Short delay to ensure Serial is ready
  Serial.println(WiFi.macAddress());
}
 
void loop(){
  // Nothing to do here
}

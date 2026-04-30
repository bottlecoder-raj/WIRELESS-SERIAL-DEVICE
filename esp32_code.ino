#include <esp_now.h>
#include <WiFi.h>

HardwareSerial mySerial(2);  // UART2

uint8_t broadcastAddress[] = {0xD4, 0x8A, 0xFC, 0xCF, 0x19, 0x9C}; 

void OnDataSent(const wifi_tx_info_t *info, esp_now_send_status_t status) {}

void OnDataRecv(const esp_now_recv_info *recv_info, const uint8_t *incomingData, int len) {
  Serial.write(incomingData, len); // Print received ESP-NOW data
}

void setup() {
  Serial.begin(115200);  // PC monitor
  mySerial.begin(115200, SERIAL_8N1, 16, 17); // RX, TX  👈 IMPORTANT

  WiFi.mode(WIFI_STA);
  Serial.print("ESP32 MAC Address: ");
  delay(1000); // Short delay to ensure Serial is ready
  Serial.println(WiFi.macAddress());

  if (esp_now_init() != ESP_OK) return;

  esp_now_register_send_cb(OnDataSent);
  esp_now_register_recv_cb(OnDataRecv);
  
  esp_now_peer_info_t peerInfo = {};
  memcpy(peerInfo.peer_addr, broadcastAddress, 6);
  peerInfo.channel = 0;  
  peerInfo.encrypt = false;
  
  if (esp_now_add_peer(&peerInfo) != ESP_OK) return;
}

void loop() {
  int availableBytes = mySerial.available();   // 👈 FIXED
  int SerialBytes = Serial.available();
  if (availableBytes > 0 || SerialBytes > 0) {
    int len = min(availableBytes, 250);
    int len2= min(SerialBytes,250);
    uint8_t buffer[250];
    int readLen = mySerial.readBytes(buffer, len) + Serial.readBytes(buffer,len2);  // 👈 FIXED
    esp_now_send(broadcastAddress, buffer, readLen);
  }
}
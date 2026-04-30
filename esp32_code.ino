#include <esp_now.h>
#include <WiFi.h>

// REPLACE WITH THE MAC ADDRESS OF THE RECEIVER
uint8_t broadcastAddress[] = {0xD4, 0x8A, 0xFC, 0xCF, 0x19, 0x9C}; 

void OnDataSent(const wifi_tx_info_t *info, esp_now_send_status_t status) {
  // Optional: Serial.println(status == ESP_NOW_SEND_SUCCESS ? "OK" : "Error");
}

void OnDataRecv(const esp_now_recv_info *recv_info, const uint8_t *incomingData, int len) {
  // Push incoming radio data to Serial instantly
  Serial.write(incomingData, len);
}

void setup() {
  // High baud rate recommended for continuous data
  Serial.begin(115200);
  WiFi.mode(WIFI_STA);

  if (esp_now_init() != ESP_OK) {
    return;
  }

  esp_now_register_send_cb(OnDataSent);
  esp_now_register_recv_cb(OnDataRecv);
  
  esp_now_peer_info_t peerInfo = {};
  memcpy(peerInfo.peer_addr, broadcastAddress, 6);
  peerInfo.channel = 0;  
  peerInfo.encrypt = false;
  
  if (esp_now_add_peer(&peerInfo) != ESP_OK){
    return;
  }
}

void loop() {
  // CHECK: Is there data in the Serial buffer?
  int availableBytes = Serial.available();
  
  if (availableBytes > 0) {
    // Limit to the ESP-NOW max payload (250 bytes)
    int len = (availableBytes > 250) ? 250 : availableBytes;
    
    uint8_t buffer[len];
    
    // READ: Grab only what is currently there (Non-blocking)
    Serial.readBytes(buffer, len);
    
    // SEND: Push to radio immediately
    esp_now_send(broadcastAddress, buffer, len);
  }
}
#include <esp_now.h>
#include <WiFi.h>

// REPLACE WITH THE MAC ADDRESS OF THE OTHER ESP32
uint8_t broadcastAddress[] = {0xD4, 0x8A, 0xFC, 0xD0, 0xC8, 0xF8};  //Check for MAC Address usimg the MAC_Address_Tester.ino


// FIXED: Updated signature for Send Callback (v3.0+)
// Changed const uint8_t *mac_addr to const wifi_tx_info_t *info
void OnDataSent(const wifi_tx_info_t *info, esp_now_send_status_t status) {
  // status == ESP_NOW_SEND_SUCCESS ? "Success" : "Fail"
}

// FIXED: Updated signature for Receive Callback (v3.0+)
void OnDataRecv(const esp_now_recv_info *recv_info, const uint8_t *incomingData, int len) {
  // Forward everything received over air to the Serial port
  Serial.write(incomingData, len);
}

void setup() {
  Serial.begin(115200);
  WiFi.mode(WIFI_STA);

  if (esp_now_init() != ESP_OK) {
    Serial.println("Error initializing ESP-NOW");
    return;
  }

  // Registering callbacks
  esp_now_register_send_cb(OnDataSent);
  esp_now_register_recv_cb(OnDataRecv);
  
  // Register peer
  esp_now_peer_info_t peerInfo = {};
  memcpy(peerInfo.peer_addr, broadcastAddress, 6);
  peerInfo.channel = 0;  
  peerInfo.encrypt = false;
  
  if (esp_now_add_peer(&peerInfo) != ESP_OK){
    Serial.println("Failed to add peer");
    return;
  }
}

void loop() {
  // Read from Serial (PC/RPi) and send via ESP-NOW
  if (Serial.available()) {
    uint8_t buffer[250]; 
    int len = Serial.readBytes(buffer, sizeof(buffer));
    if (len > 0) {
      esp_now_send(broadcastAddress, buffer, len);
    }
  }
}

#include <Arduino.h> 
#include <BLEDevice.h>
#include <BLEUtils.h>
#include <BLEServer.h>
#include <ESP32Servo.h>
#include <BLE2902.h>

// BLE Identifiers
#define SERVICE_UUID "b36ffaec-2ef4-4f92-8240-05877b9d71e6"
#define RX_UUID "36e89808-bb82-471d-9791-a2dc10994675"
#define TX_UUID "c6b9e79d-8f5c-4cc0-9628-04cdd5a05bd8"

// BLECharacteristic Objects for TX | RX
BLECharacteristic *pTxChar;
BLECharacteristic *pRxChar;

// BLE Callbacks Class - Manages retrieved data
class RxCallbacks: public BLECharacteristicCallbacks {
  void onWrite(BLECharacteristic *pCharacteristic) override // onWrite : rx function for BLE communication
  {
    std::string rxValue = pCharacteristic->getValue(); // Gets string value from tx (python module)

      if (rxValue.length() == 4) // ensuring 4-bytes for 32 bit int --> Needs to be JSON?
      {
        int32_t rxInt = *(int32_t*)rxValue.data(); // Re - interprets byte -> int
      }
  }

};

void setup() {
  Serial.begin(115200);
  

  BLEDevice::init("BioCare_ProstheticESP32");
  BLEServer *pServer = BLEDevice::createServer(); // Initializes server

  BLEService *pService = pServer->createService(SERVICE_UUID);


  // Rx Characterstic (Write Preset Data)
  pRxChar = pService->createCharacteristic(
      RX_UUID,
      BLECharacteristic::PROPERTY_WRITE
  );
  pRxChar->setCallbacks(new RxCallbacks());

  // Tx Characteristics (Notify / Send Data)
  pTxChar = pService->createCharacteristic(
      TX_UUID,
      BLECharacteristic::PROPERTY_NOTIFY

  );
  pTxChar->addDescriptor(new BLE2902()); // BLE2902 CCCD that allows for notifications using notify()

  pService->start();
  BLEDevice::startAdvertising();

  Serial.print("BLE Service open to Pairing...");
}

void loop() {
}

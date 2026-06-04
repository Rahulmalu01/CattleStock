#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>
const char* ssid = "Rahul Home";
const char* password = "nahipatta";

// CHANGE THIS TO YOUR PC'S IP ADDRESS
const char* API_URL =
"http://192.168.0.101:8000/api/hardware/sensor-data/";

const char* API_KEY =
"cattlecare-hardware-bv7trywqe9ryncwp8%$&rbrieu2uh&{eu";

String cattleIds[] = {
  "COW_001",
  "COW_002",
  "COW_003",
  "COW_004"
};

String rfidTags[] = {
  "RFID_001",
  "RFID_002",
  "RFID_003",
  "RFID_004"
};

float randomFloat(float minVal, float maxVal) {
  return minVal +
         ((float)random(0, 1000) / 1000.0) *
         (maxVal - minVal);
}

void connectWiFi() {

  Serial.print("Connecting to WiFi");

  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println();
  Serial.println("WiFi Connected");

  Serial.print("ESP IP: ");
  Serial.println(WiFi.localIP());
}

void setup() {

  Serial.begin(115200);

  randomSeed(analogRead(A0));

  connectWiFi();
}

void loop() {

  if (WiFi.status() != WL_CONNECTED) {
    connectWiFi();
  }

  int cow = random(0, 4);

  float bodyTemp = randomFloat(37.5, 40.5);
  int heartRate = random(60, 90);
  int respiratoryRate = random(20, 35);
  int steps = random(1000, 5000);
  int battery = random(20, 100);
  float milkYield = randomFloat(18.0, 32.0);

  String jsonData = "{";

  jsonData += "\"device\":{";
  jsonData += "\"device_id\":\"" + rfidTags[cow] + "\",";
  jsonData += "\"device_name\":\"Collar Sensor\",";
  jsonData += "\"device_type\":\"collar\",";
  jsonData += "\"firmware_version\":\"1.0.0\"";
  jsonData += "},";

  jsonData += "\"cattle\":{";
  jsonData += "\"cattle_id\":\"" + cattleIds[cow] + "\",";
  jsonData += "\"rfid_tag\":\"" + rfidTags[cow] + "\"";
  jsonData += "},";

  jsonData += "\"readings\":{";

  jsonData += "\"vital_signs\":{";
  jsonData += "\"body_temperature\":" + String(bodyTemp, 2) + ",";
  jsonData += "\"heart_rate\":" + String(heartRate) + ",";
  jsonData += "\"respiratory_rate\":" + String(respiratoryRate);
  jsonData += "},";

  jsonData += "\"activity\":{";
  jsonData += "\"steps\":" + String(steps) + ",";
  jsonData += "\"activity_duration_minutes\":" + String(random(120, 400)) + ",";
  jsonData += "\"activity_level\":\"normal\"";
  jsonData += "},";

  jsonData += "\"rumination\":{";
  jsonData += "\"rumination_duration_minutes\":" + String(random(250, 500)) + ",";
  jsonData += "\"rumination_episodes\":" + String(random(4, 12)) + ",";
  jsonData += "\"rumination_quality\":\"good\"";
  jsonData += "},";

  jsonData += "\"behavior\":{";
  jsonData += "\"eating_duration_minutes\":" + String(random(100, 250)) + ",";
  jsonData += "\"lying_duration_minutes\":" + String(random(400, 650)) + ",";
  jsonData += "\"standing_duration_minutes\":" + String(random(150, 350)) + ",";
  jsonData += "\"walking_duration_minutes\":" + String(random(100, 300));
  jsonData += "},";

  jsonData += "\"milk\":{";
  jsonData += "\"milk_yield_liters\":" + String(milkYield, 2) + ",";
  jsonData += "\"milk_conductivity\":" + String(randomFloat(3.8, 5.0), 2);
  jsonData += "},";

  jsonData += "\"feeding\":{";
  jsonData += "\"feeding_efficiency_percent\":" + String(randomFloat(75, 98), 2) + ",";
  jsonData += "\"feed_intake_estimated\":true";
  jsonData += "}";

  jsonData += "},";

  jsonData += "\"device_status\":{";
  jsonData += "\"battery_level_percent\":" + String(battery) + ",";
  jsonData += "\"signal_strength_percent\":" + String(random(50, 100)) + ",";
  jsonData += "\"gps_accuracy\":\"high\"";
  jsonData += "},";

  jsonData += "\"data_quality\":{";
  jsonData += "\"quality_score\":95,";
  jsonData += "\"data_points_received\":24,";
  jsonData += "\"data_points_expected\":24";
  jsonData += "}";

  jsonData += "}";

  Serial.println();
  Serial.println("Sending Data:");
  Serial.println(jsonData);

  WiFiClient client;
  HTTPClient http;

  http.begin(client, API_URL);

  http.addHeader(
    "Content-Type",
    "application/json"
  );

  http.addHeader(
    "X-API-KEY",
    API_KEY
  );

  int httpResponseCode =
    http.POST(jsonData);

  Serial.print("HTTP Response Code: ");
  Serial.println(httpResponseCode);

  if (httpResponseCode > 0) {

    String response =
      http.getString();

    Serial.println("Server Response:");
    Serial.println(response);

  } else {

    Serial.print("POST Failed: ");
    Serial.println(
      http.errorToString(httpResponseCode)
    );
  }

  http.end();

  delay(30000);
}
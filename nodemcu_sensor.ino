#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>
#include <DHT.h>

// Konfigurasi WiFi
const char* ssid = "YOUR_WIFI_SSID";        // Ganti dengan SSID WiFi kamu
const char* password = "YOUR_WIFI_PASSWORD"; // Ganti dengan password WiFi

// Konfigurasi server Django
const char* serverUrl = "http://192.168.1.100:8000/api/sensor-data/"; // Ganti dengan IP komputer Django server

// Konfigurasi DHT22
#define DHTPIN D4     // Pin data DHT22 (GPIO 2)
#define DHTTYPE DHT22 // Tipe sensor DHT
DHT dht(DHTPIN, DHTTYPE);

// ID ruangan (sesuaikan dengan database Django)
int roomId = 1; // Ganti dengan ID room yang sesuai

void setup() {
  Serial.begin(115200);
  dht.begin();

  // Koneksi WiFi
  WiFi.begin(ssid, password);
  Serial.print("Connecting to WiFi");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
}

void loop() {
  // Baca data dari DHT22
  float temperature = dht.readTemperature();
  float humidity = dht.readHumidity();

  // Cek apakah pembacaan berhasil
  if (isnan(temperature) || isnan(humidity)) {
    Serial.println("Failed to read from DHT sensor!");
    delay(2000);
    return;
  }

  // Tampilkan data di Serial Monitor
  Serial.print("Temperature: ");
  Serial.print(temperature);
  Serial.print(" °C, Humidity: ");
  Serial.print(humidity);
  Serial.println(" %");

  // Kirim data ke server Django
  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;
    http.begin(serverUrl);
    http.addHeader("Content-Type", "application/json");

    // Buat payload JSON
    String jsonPayload = "{";
    jsonPayload += "\"room_id\":" + String(roomId) + ",";
    jsonPayload += "\"temperature\":" + String(temperature, 2) + ",";
    jsonPayload += "\"humidity\":" + String(humidity, 2);
    jsonPayload += "}";

    Serial.println("Sending data: " + jsonPayload);

    int httpResponseCode = http.POST(jsonPayload);

    if (httpResponseCode > 0) {
      String response = http.getString();
      Serial.println("HTTP Response code: " + String(httpResponseCode));
      Serial.println("Response: " + response);
    } else {
      Serial.println("Error on sending POST: " + String(httpResponseCode));
    }

    http.end();
  } else {
    Serial.println("WiFi not connected!");
  }

  // Tunggu 10 detik sebelum pengukuran berikutnya
  delay(10000);
}

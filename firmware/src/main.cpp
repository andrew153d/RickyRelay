#include <Arduino.h>

#define RELAY_A 10
#define RELAY_B 11

#include "Arduino.h"
#include "AsyncOTA.h"
#include "WIFI.h"
#include "ESPmDNS.h"

AsyncWebServer server(80);

const char *hostname = "clicky";
const char *ssid = "GrowWifi";
const char *password = "T4*15KpHi1bj";

void setup()
{
  Serial.begin(115200);
  Serial.setTimeout(5);

  Serial.print("WIFI init");
  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);
  // Wait for connection
  while (WiFi.status() != WL_CONNECTED)
  {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.print("Connected to ");
  Serial.println(ssid);
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());

  // Make it possible to access webserver at http://myEsp32.local
  if (!MDNS.begin(hostname))
  {
    Serial.println("Error setting up mDNS responder!");
  }
  else
  {
    Serial.printf("Access at http://%s.local\n", hostname);
  }

  // Show a link to OTA page at http://myEsp32.local
  server.on("/", HTTP_GET, [](AsyncWebServerRequest *request)
            {
        String html = "<html><body>";
    html += "<a href=\"/ota\">Update Software</a>";
    html += "</body></html>";
    request->send(200, "text/html", html); });

  AsyncOTA.begin(&server);
  server.begin();

  pinMode(RELAY_A, OUTPUT);
  pinMode(RELAY_B, OUTPUT);
}

void loop()
{
  while (!Serial.available())
  {
    delay(10);
  }
  // Read the input string and trim any unnecessary whitespace
  Serial.println("Received command:");
  String result = Serial.readString();
  result.trim(); // Remove any leading or trailing whitespace

  // Print the received command
  Serial.println("Received command: " + result);

  // Command for Relay A
  if (result == "AON")
  {
    digitalWrite(RELAY_A, HIGH);
    Serial.println("Turning on Relay A");
  }
  else if (result == "AOFF")
  {
    digitalWrite(RELAY_A, LOW);
    Serial.println("Turning off Relay A");
  }
  // Command for Relay B
  else if (result == "BON")
  {
    digitalWrite(RELAY_B, HIGH);
    Serial.println("Turning on Relay B");
  }
  else if (result == "BOFF")
  {
    digitalWrite(RELAY_B, LOW);
    Serial.println("Turning off Relay B");
  }
  // Invalid command
  else
  {
    Serial.println("Invalid command received.");
  }
}

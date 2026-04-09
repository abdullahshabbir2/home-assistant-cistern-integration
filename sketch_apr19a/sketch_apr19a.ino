#include <WiFi.h>
#include <WebServer.h>
#include <ArduinoJson.h>
#include <ESPmDNS.h>
#include "secrets.h"

// ——— CONFIG —————————————————————————————————————
const uint16_t HTTP_PORT  = 80;
const char* DEVICE_ID     = "cistern_001";
const char* SERIAL_NUMBER = "SN123456";
// ————————————————————————————————————————————————

WebServer server(HTTP_PORT);

// ——— DeviceState Definition —————————————————————————
struct DeviceState {
  float  fill_level_percent;
  int    fill_level_liter;
  float  fill_level_height;
  const char* filter_status;
  int    extraction_pumps_active;
  int    time_controlled_outlets_active;
  int    refill_appliances_active;
  int    drainage_appliances_active;
  int    filter_check_appliances_active;
  int    irrigation_valves_active;
  float  expected_precipitation_lpm2;
  float  historic_precipitation_lpm2;
  int    expected_inflow_liters;
  String planned_irrigation_start_zone1;
  String planned_irrigation_end_zone1;
  String planned_irrigation_start_zone2;
  String planned_irrigation_end_zone2;
  String planned_irrigation_start_zone3;
  String planned_irrigation_end_zone3;
  String planned_irrigation_start_zone4;
  String planned_irrigation_end_zone4;
  String planned_irrigation_start_zone5;
  String planned_irrigation_end_zone5;
  String planned_irrigation_start_zone6;
  String planned_irrigation_end_zone6;
  String planned_irrigation_start_zone7;
  String planned_irrigation_end_zone7;
  String planned_irrigation_start_zone8;
  String planned_irrigation_end_zone8;
  const char* operating_mode;
  const char* error;
};

// ——— DeviceConfig Definition ————————————————————————
struct DeviceConfig {
  // Relays
  int    relay_control[8]                = {0};
  // Irrigation zones
  int    zone_area[8]                    = {0};
  int    zone_manual[8]                  = {0};
  int    zone_optimization[8]            = {0};
  int    zone_demand[8]                  = {0};
  // Global irrigation
  int    irrigation_optimization_level   = 0;
  int    split_irrigation                = 0;
  String irrigation_start_time_one       = "00:00";
  String irrigation_start_time_two       = "00:00";
  int    max_manual_irrigation_duration  = 0;
  // Outlet functions
  int    outlet_configuration[8]         = {0};
  int    switch_time_controlled_outlets  = 0;
  // Sensors & thresholds
  int    filter_sensor_active            = 0;
  int    flow_manual_definition          = 0;
  int    flow_sensor_active              = 0;
  int    level_sensor_active             = 0;
  int    flow_sensor_max_volume          = 0;
  int    level_controller_mode           = 0;
  int    lower_level_controller_threshold= 0;
  int    upper_level_controller_threshold= 0;
  int    warning_threshold               = 0;
  // Tank configuration
  int    tank_pre_defined_model          = 0;
  int    number_of_tanks                 = 0;
  int    manual_tank_form_definition     = 0;
  float  tank_measure_A_meters           = 0.0;
  float  tank_measure_B_meters           = 0.0;
  float  tank_measure_C_meters           = 0.0;
  int    max_refill_duration_minutes     = 0;
  int    collection_surface_sqm          = 0;
} config;

// ——— Helpers —————————————————————————————————————
String getIsoTimestamp() {
  uint32_t s = millis() / 1000;
  char buf[32];
  snprintf(buf, sizeof(buf),
           "2025-04-07T12:%02u:%02uZ",
           (s/60)%60, s%60);
  return String(buf);
}
String randomTime(int hour) {
  int minute = random(0, 60);
  char buf[6];
  snprintf(buf, sizeof(buf), "%02d:%02d", hour, minute);
  return String(buf);
}
const char* randomOutletConfig(int zone) {
  int idx = random(0,3);
  if (idx == 0) return "extraction pump";
  if (idx == 1) return "refill appliance";
  static char buf[32];
  snprintf(buf, sizeof(buf), "irrigation valve zone %d", zone);
  return buf;
}
// ————————————————————————————————————————————————

// ——— Randomize State —————————————————————————————————
DeviceState randomizeState() {
  DeviceState s;
  s.fill_level_percent            = random(0, 101) + random(0,100)/100.0;
  s.fill_level_liter              = random(0, 1000);
  s.fill_level_height             = random(0, 500)/100.0;
  s.filter_status                 = random(0, 2) ? "clean" : "dirty";
  s.extraction_pumps_active       = random(0, 5);
  s.time_controlled_outlets_active= random(0, 5);
  s.refill_appliances_active      = random(0, 5);
  s.drainage_appliances_active    = random(0, 5);
  s.filter_check_appliances_active= random(0, 5);
  s.irrigation_valves_active      = random(0, 9);
  s.expected_precipitation_lpm2   = random(0, 1001)/100.0;
  s.historic_precipitation_lpm2   = random(0, 2001)/100.0;
  s.expected_inflow_liters        = random(0, 5000);
  for (int i = 1; i <= 8; i++) {
    s.planned_irrigation_start_zone1 = randomTime(5+i);
    s.planned_irrigation_end_zone1   = randomTime(5+i);
  }
  s.operating_mode                 = random(0,2) ? "Automatic" : "Manual";
  s.error                          = "None";
  return s;
}

// ——— HTTP Handlers ——————————————————————————————————
void handleStatus() {
  DeviceState st = randomizeState();
  // big enough: telemetry + 60 config fields
  StaticJsonDocument<8192> doc;

  // — Telemetry —
  doc["device_id"]            = DEVICE_ID;
  doc["device_name"]          = DEVICE_ID;
  doc["serial_number"]        = SERIAL_NUMBER;
  doc["ip_address"]           = WiFi.localIP().toString();
  doc["mac_address"]          = WiFi.macAddress();
  doc["connected_to_network"] = WIFI_SSID;
  doc["fill_level_percent"]   = st.fill_level_percent;
  doc["fill_level_liter"]     = st.fill_level_liter;
  doc["fill_level_height"]    = st.fill_level_height;
  for (int i = 1; i <= 8; i++) {
    doc[String("outlet_configuration_") + i] = randomOutletConfig(i);
  }
  doc["filter_status"]                     = st.filter_status;
  doc["extraction_pumps_active"]           = st.extraction_pumps_active;
  doc["time_controlled_outlets_active"]    = st.time_controlled_outlets_active;
  doc["refill_appliances_active"]          = st.refill_appliances_active;
  doc["drainage_appliances_active"]        = st.drainage_appliances_active;
  doc["filter_check_appliances_active"]    = st.filter_check_appliances_active;
  doc["irrigation_valves_active"]          = st.irrigation_valves_active;
  doc["expected_precipitation_litres_per_sqm"] = st.expected_precipitation_lpm2;
  doc["historic_precipitation_litres_per_sqm"] = st.historic_precipitation_lpm2;
  doc["expected_inflow_litres"]                = st.expected_inflow_liters;
  for (int i = 1; i <= 8; i++) {
    doc[String("planned_irrigation_start_zone") + i] = randomTime(5 + i);
    doc[String("planned_irrigation_end_zone")   + i] = randomTime(5 + i);
  }
  doc["operating_mode"] = st.operating_mode;
  doc["error"]          = nullptr;
  doc["timestamp"]      = getIsoTimestamp();

  // — Mirror back configuration —
  for (int i = 1; i <= 8; i++) {
    doc[String("relay_control_")          + i] = config.relay_control[i-1];
    doc[String("irrigation_zone")         + i + "_area"]                    = config.zone_area[i-1];
    doc[String("irrigation_zone")         + i + "_manual"]                  = config.zone_manual[i-1];
    doc[String("irrigation_zone")         + i + "_optimization_active"]     = config.zone_optimization[i-1];
    doc[String("irrigation_zone")         + i + "_demand_litres_per_sqm"]   = config.zone_demand[i-1];
    doc[String("outlet_configuration_")   + i] = config.outlet_configuration[i-1];
  }
  doc["irrigation_optimization_level"]    = config.irrigation_optimization_level;
  doc["split_irrigation"]                 = config.split_irrigation;
  doc["irrigation_start_time_one"]        = config.irrigation_start_time_one;
  doc["irrigation_start_time_two"]        = config.irrigation_start_time_two;
  doc["max_manual_irrigation_duration"]   = config.max_manual_irrigation_duration;
  doc["switch_time_controlled_outlets"]   = config.switch_time_controlled_outlets;
  doc["filter_sensor_active"]             = config.filter_sensor_active;
  doc["flow_manual_definition"]           = config.flow_manual_definition;
  doc["flow_sensor_active"]               = config.flow_sensor_active;
  doc["level_sensor_active"]              = config.level_sensor_active;
  doc["flow_sensor_max_volume"]           = config.flow_sensor_max_volume;
  doc["level_controller_mode"]            = config.level_controller_mode;
  doc["lower_level_controller_threshold"] = config.lower_level_controller_threshold;
  doc["upper_level_controller_threshold"] = config.upper_level_controller_threshold;
  doc["warning_threshold"]                = config.warning_threshold;
  doc["tank_pre_defined_model"]           = config.tank_pre_defined_model;
  doc["number_of_tanks"]                  = config.number_of_tanks;
  doc["manual_tank_form_definition"]      = config.manual_tank_form_definition;
  doc["tank_measure_A_meters"]            = config.tank_measure_A_meters;
  doc["tank_measure_B_meters"]            = config.tank_measure_B_meters;
  doc["tank_measure_C_meters"]            = config.tank_measure_C_meters;
  doc["max_refill_duration_minutes"]      = config.max_refill_duration_minutes;
  doc["collection_surface_sqm"]           = config.collection_surface_sqm;

  String out;
  serializeJson(doc, out);
  server.send(200, "application/json", out);
}

void handleCommand() {
  // 1) ACK immediately so Home Assistant does not hang
  server.send(200, "application/json", "{\"status\":\"ok\"}");

  // 2) Grab body
  String body = server.arg("plain");
  if (body.length() == 0) return;

  // 3) Parse JSON into a small buffer for speed
  StaticJsonDocument<1024> doc;
  DeserializationError err = deserializeJson(doc, body);
  if (err) {
    Serial.print(F("JSON parse error: "));
    Serial.println(err.c_str());
    return;
  }

  // 4) Validate command
  const char* command = doc["command"];
  if (!command || strcmp(command, "update_device") != 0) return;

  // 5) Bail if no parameters
  if (!doc.containsKey("parameters")) return;
  JsonObject p = doc["parameters"];

  //
  // 6) RELAYS (nested + flat)
  //
  if (JsonObject rc = p["relay_control"]) {
    for (int i = 1; i <= 8; i++) {
      int v = rc["relay_control_" + String(i)] | -1;
      if (v >= 0) config.relay_control[i-1] = v;
    }
  }
  for (int i = 1; i <= 8; i++) {
    int v = p["relay_control_" + String(i)] | -1;
    if (v >= 0) config.relay_control[i-1] = v;
  }

  //
  // 7) IRRIGATION (global only)
  //
  if (JsonObject irr = p["irrigation"]) {
    config.irrigation_optimization_level = irr["irrigation_optimization_level"] | config.irrigation_optimization_level;
    config.split_irrigation              = irr["split_irrigation"]             | config.split_irrigation;
    if (irr.containsKey("irrigation_start_time_one"))
      config.irrigation_start_time_one = String(irr["irrigation_start_time_one"].as<const char*>());
    if (irr.containsKey("irrigation_start_time_two"))
      config.irrigation_start_time_two = String(irr["irrigation_start_time_two"].as<const char*>());
    config.max_manual_irrigation_duration = irr["max_manual_irrigation_duration"] | config.max_manual_irrigation_duration;
  }

  //
  // 8) OUTLET FUNCTIONS
  //
  if (JsonObject of = p["outlet_functions"]) {
    for (int i = 1; i <= 8; i++) {
      config.outlet_configuration[i-1] = of["outlet_configuration_" + String(i)] | config.outlet_configuration[i-1];
    }
    config.switch_time_controlled_outlets = of["switch_time_controlled_outlets"] | config.switch_time_controlled_outlets;
  }

  //
  // 9) FLAG SWITCHES (nested under sensors + flat)
  //
  if (JsonObject s = p["sensors"]) {
    config.filter_sensor_active        = s["filter_sensor_active"]        | config.filter_sensor_active;
    config.flow_manual_definition      = s["flow_manual_definition"]      | config.flow_manual_definition;
    config.flow_sensor_active          = s["flow_sensor_active"]          | config.flow_sensor_active;
    config.level_sensor_active         = s["level_sensor_active"]         | config.level_sensor_active;
    config.manual_tank_form_definition = s["manual_tank_form_definition"] | config.manual_tank_form_definition;
  }
  config.filter_sensor_active        = p["filter_sensor_active"]        | config.filter_sensor_active;
  config.flow_manual_definition      = p["flow_manual_definition"]      | config.flow_manual_definition;
  config.flow_sensor_active          = p["flow_sensor_active"]          | config.flow_sensor_active;
  config.level_sensor_active         = p["level_sensor_active"]         | config.level_sensor_active;
  config.manual_tank_form_definition = p["manual_tank_form_definition"] | config.manual_tank_form_definition;
  config.split_irrigation            = p["split_irrigation"]            | config.split_irrigation;
  config.switch_time_controlled_outlets = p["switch_time_controlled_outlets"] | config.switch_time_controlled_outlets;

  //
  // 10) TANK CONFIGURATION
  //
  if (JsonObject t = p["tank_configuration"]) {
    config.tank_pre_defined_model      = t["tank_pre_defined_model"]      | config.tank_pre_defined_model;
    config.number_of_tanks             = t["number_of_tanks"]             | config.number_of_tanks;
    config.manual_tank_form_definition = t["manual_tank_form_definition"] | config.manual_tank_form_definition;
    config.tank_measure_A_meters       = t["tank_measure_A_meters"]       | config.tank_measure_A_meters;
    config.tank_measure_B_meters       = t["tank_measure_B_meters"]       | config.tank_measure_B_meters;
    config.tank_measure_C_meters       = t["tank_measure_C_meters"]       | config.tank_measure_C_meters;
    config.max_refill_duration_minutes = t["max_refill_duration_minutes"] | config.max_refill_duration_minutes;
    config.collection_surface_sqm      = t["collection_surface_sqm"]      | config.collection_surface_sqm;
  }

  //
  // 11) Timestamp - print at end
  //
  if (doc.containsKey("timestamp")) {
    const char* ts = doc["timestamp"].as<const char*>();
    Serial.printf("timestamp = %s\n", ts);
  }

  //print all configurations
  printConfig();
}

void handleNotFound() {
  server.send(404, "text/plain", "Not found");
}

void printConfig() {
  // Preallocate enough space for all lines (adjust as needed)
  String out;
  out.reserve(800);

  out += "\n=== Current DeviceConfig ===\n";

  // Relays
  for (int i = 0; i < 8; i++) {
    out += "relay_control_";
    out += String(i + 1);
    out += " = ";
    out += String(config.relay_control[i]);
    out += '\n';
  }

  // Irrigation zones
  for (int i = 0; i < 8; i++) {
    out += "irrigation_zone";
    out += String(i + 1);
    out += "_area = ";
    out += String(config.zone_area[i]);
    out += '\n';

    out += "irrigation_zone";
    out += String(i + 1);
    out += "_manual = ";
    out += String(config.zone_manual[i]);
    out += '\n';

    out += "irrigation_zone";
    out += String(i + 1);
    out += "_optimization_active = ";
    out += String(config.zone_optimization[i]);
    out += '\n';

    out += "irrigation_zone";
    out += String(i + 1);
    out += "_demand_litres_per_sqm = ";
    out += String(config.zone_demand[i]);
    out += '\n';
  }

  // Global irrigation
  out += "irrigation_optimization_level = ";
  out += String(config.irrigation_optimization_level);
  out += '\n';

  out += "split_irrigation = ";
  out += String(config.split_irrigation);
  out += '\n';

  out += "irrigation_start_time_one = ";
  out += config.irrigation_start_time_one;
  out += '\n';

  out += "irrigation_start_time_two = ";
  out += config.irrigation_start_time_two;
  out += '\n';

  out += "max_manual_irrigation_duration = ";
  out += String(config.max_manual_irrigation_duration);
  out += '\n';

  // Outlets
  for (int i = 0; i < 8; i++) {
    out += "outlet_configuration_";
    out += String(i + 1);
    out += " = ";
    out += String(config.outlet_configuration[i]);
    out += '\n';
  }
  out += "switch_time_controlled_outlets = ";
  out += String(config.switch_time_controlled_outlets);
  out += '\n';

  // Sensors & thresholds
  out += "filter_sensor_active = ";
  out += String(config.filter_sensor_active);
  out += '\n';
  out += "flow_manual_definition = ";
  out += String(config.flow_manual_definition);
  out += '\n';
  out += "flow_sensor_active = ";
  out += String(config.flow_sensor_active);
  out += '\n';
  out += "level_sensor_active = ";
  out += String(config.level_sensor_active);
  out += '\n';
  out += "flow_sensor_max_volume = ";
  out += String(config.flow_sensor_max_volume);
  out += '\n';
  out += "level_controller_mode = ";
  out += String(config.level_controller_mode);
  out += '\n';
  out += "lower_level_controller_threshold = ";
  out += String(config.lower_level_controller_threshold);
  out += '\n';
  out += "upper_level_controller_threshold = ";
  out += String(config.upper_level_controller_threshold);
  out += '\n';
  out += "warning_threshold = ";
  out += String(config.warning_threshold);
  out += '\n';

  // Tank configuration
  out += "tank_pre_defined_model = ";
  out += String(config.tank_pre_defined_model);
  out += '\n';
  out += "number_of_tanks = ";
  out += String(config.number_of_tanks);
  out += '\n';
  out += "manual_tank_form_definition = ";
  out += String(config.manual_tank_form_definition);
  out += '\n';
  out += "tank_measure_A_meters = ";
  out += String(config.tank_measure_A_meters, 2);
  out += '\n';
  out += "tank_measure_B_meters = ";
  out += String(config.tank_measure_B_meters, 2);
  out += '\n';
  out += "tank_measure_C_meters = ";
  out += String(config.tank_measure_C_meters, 2);
  out += '\n';
  out += "max_refill_duration_minutes = ";
  out += String(config.max_refill_duration_minutes);
  out += '\n';
  out += "collection_surface_sqm = ";
  out += String(config.collection_surface_sqm);
  out += '\n';

  out += "=== End of DeviceConfig ===\n";

  // Single print call
  Serial.print(out);
}


void setup() {
  Serial.begin(115200);
  randomSeed(micros());
  Serial.println("\nStarting Cistern controller...");

  // Wi-Fi
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  Serial.printf("Connecting to %s", WIFI_SSID);
  while (WiFi.status() != WL_CONNECTED) {
    delay(300); Serial.print(".");
  }
  Serial.printf("\nConnected, IP=%s\n", WiFi.localIP().toString().c_str());

  // mDNS
  if (!MDNS.begin("esp32-cistern")) {
    Serial.println("mDNS failed");
  } else {
    MDNS.addService("cistern","tcp",HTTP_PORT);
    Serial.println("mDNS responder started");
  }

  // HTTP
  server.on("/status", HTTP_GET,  handleStatus);
  server.on("/command", HTTP_POST, handleCommand);
  server.onNotFound(handleNotFound);
  server.begin();
  Serial.printf("HTTP server listening on port %u\n", HTTP_PORT);
}

void loop() {
  server.handleClient();
}

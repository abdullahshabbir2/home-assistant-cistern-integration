# Cistern Controller Home Assistant Integration

[![Home Assistant Custom Integration](https://img.shields.io/badge/Home%20Assistant-Custom%20Integration-41BDF5?logo=homeassistant&logoColor=white)](https://www.home-assistant.io/)
![ESP32 Firmware](https://img.shields.io/badge/ESP32-Firmware-E7352C)
![Python Backend](https://img.shields.io/badge/Python-Backend-3776AB?logo=python&logoColor=white)
![Arduino](https://img.shields.io/badge/Arduino-Framework-00979D?logo=arduino&logoColor=white)
![REST API](https://img.shields.io/badge/API-REST-0A7EA4)

An end-to-end IoT portfolio project centered on a custom Home Assistant integration for a cistern controller, paired with ESP32 firmware for local monitoring, irrigation scheduling, and device control over a REST API.

This repository is strong portfolio material because it shows work across embedded systems, backend integration, local networking, and home automation UX in one project.

## Portfolio Highlights

- Custom Home Assistant integration design
- ESP32 firmware exposing a local REST API
- Device discovery and polling
- Interactive entities for switches, numbers, and time controls
- Dashboard configuration for the Home Assistant frontend

## What It Does

The project is built around a custom `cistern` integration for Home Assistant. The integration connects Home Assistant to a cistern controller over the local network, reads telemetry from `/status`, and sends configuration changes to `/command`.

The current ESP32 sketch is useful as a development and demo controller because it generates representative telemetry and accepts control updates. That makes the project easy to showcase without requiring a fully wired physical installation during review.

## Why It Stands Out

- Demonstrates both firmware and software integration work
- Uses a clean client-device model with `/status` and `/command` endpoints
- Exposes real user controls through Home Assistant entities
- Includes an example dashboard for the frontend layer
- Is structured so it can be reviewed quickly by recruiters or clients

## Tech Stack

- Python
- Home Assistant custom components
- ESP32 / Arduino
- REST / JSON
- YAML dashboard configuration

## Repository Structure

```text
custom_components/cistern/   Home Assistant integration
sketch_apr19a/               ESP32 firmware sketch
examples/dashboard.yaml      Example Home Assistant dashboard
assets/screenshots/          README images and demo screenshots
```

## Key Features

- Zeroconf-based device discovery for the custom integration
- Coordinator-based polling for device state updates
- Sensor entities for telemetry and operating data
- Switch entities for relay and feature toggles
- Number entities for irrigation, tank, and threshold settings
- Time entities for irrigation scheduling
- Example Lovelace dashboard configuration

## Local Setup

### Home Assistant

1. Copy `custom_components/cistern/` into your Home Assistant `config/custom_components/` directory.
2. Restart Home Assistant.
3. Add the integration from the UI and enter the ESP32 host and port if discovery does not find it automatically.

### ESP32 Firmware

1. Open `sketch_apr19a/secrets.example.h`.
2. Create a local `sketch_apr19a/secrets.h` with your Wi-Fi credentials.
3. Flash `sketch_apr19a/sketch_apr19a.ino` to an ESP32 board.

`sketch_apr19a/secrets.h` is intentionally ignored by git so credentials are not published.

## Screenshots

The current repository includes dashboard screenshots that show the main monitoring and control surfaces exposed through Home Assistant.

![Main dashboard](assets/screenshots/main_dashboard.jpeg)
![Relay control](assets/screenshots/updated_relaycontrol.jpeg)
![Irrigation dashboard](assets/screenshots/irrigation_dashboard.jpeg)
![Settings view](assets/screenshots/settings.jpeg)

For an even stronger GitHub presentation, add a hardware photo and a short demo GIF later.

## Validation

This repository includes a lightweight GitHub Actions workflow that checks the Python integration for syntax issues on every push and pull request.

## Notes

- The root-level archives and notebook files are excluded from version control to keep the repository focused on source code and showcase material.
- A license can be added before publishing, but that choice should match how you want others to use your work.
- Before pushing publicly, review the screenshots once to make sure they do not expose any personal names, IP addresses, or other private details.

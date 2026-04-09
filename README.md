# Home Assistant Cistern Controller

A portfolio project that combines a custom Home Assistant integration with an ESP32-based device API for local cistern monitoring and irrigation control.

The repository demonstrates:

- Custom Home Assistant integration design
- ESP32 firmware exposing a local REST API
- Device discovery and polling
- Interactive entities for switches, numbers, and time controls
- Dashboard configuration for the Home Assistant frontend

## What It Does

The project is built around a custom `cistern` integration for Home Assistant. The integration connects to an ESP32 controller over the local network, reads telemetry from `/status`, and sends configuration changes to `/command`.

The current ESP32 sketch is useful as a development and demo controller because it generates representative telemetry and accepts control updates. That makes the project easy to showcase without requiring a fully wired physical installation during review.

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

Yes, you should upload pictures.

For a professional GitHub repo, add:

- Dashboard screenshots
- Photos of the ESP32 hardware or prototype
- A short GIF showing the Home Assistant controls updating live

Store them in `assets/screenshots/` and reference them in this README, for example:

```md
![Dashboard overview](assets/screenshots/dashboard-overview.png)
```

## Validation

This repository includes a lightweight GitHub Actions workflow that checks the Python integration for syntax issues on every push and pull request.

## Notes

- The root-level archives and notebook files are excluded from version control to keep the repository focused on source code and showcase material.
- A license can be added before publishing, but that choice should match how you want others to use your work.

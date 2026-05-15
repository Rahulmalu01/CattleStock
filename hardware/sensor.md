# CattleCare Hardware Sensor API Documentation

## Overview

The CattleCare Hardware Sensor API is designed to collect, store, and monitor real-time cattle health and activity data from IoT devices such as collar sensors and RFID ear tags.

The system uses:

- SQL Database (PostgreSQL/SQLite)
  - Sensor readings
  - Devices
  - Cattle information

- MongoDB
  - Alerts
  - Notifications
  - Dynamic event logs

---

# System Architecture

```text
IoT Device / ESP32 / Sensor
            ↓
      Hardware API
            ↓
    Django Backend API
            ↓
 ┌─────────────────────┐
 │ SQL Database        │
 │ - Sensor Readings   │
 │ - Devices           │
 │ - Cattle            │
 └─────────────────────┘
            ↓
 ┌─────────────────────┐
 │ MongoDB             │
 │ - Alerts            │
 │ - Events            │
 └─────────────────────┘
```

---

# API Base URL

```text
http://127.0.0.1:8000/api/hardware/
```

Production Example:

```text
https://yourdomain.com/api/hardware/
```

---

# Authentication

All hardware requests require an API Key.

## Header

```http
X-API-KEY: super-secret-api-key
```

---

# API Endpoints

| Endpoint            | Method | Description                |
| ------------------- | ------ | -------------------------- |
| `/sensor-data/`     | POST   | Store sensor readings      |
| `/alerts/`          | POST   | Store alerts               |
| `/latest-readings/` | GET    | Get latest sensor readings |
| `/latest-alerts/`   | GET    | Get latest alerts          |

---

# Sensor Data API

## Endpoint

```http
POST /api/hardware/sensor-data/
```

---

# Sensor Data Payload

```json
{
  "device": {
    "device_id": "RFID_001",
    "device_name": "Cattle-Bessie-CollarSensor",
    "device_type": "collar",
    "firmware_version": "2.1.0"
  },
  "cattle": {
    "rfid_tag": "RFID_001",
    "cattle_id": "COW_001"
  },
  "timestamp": "2026-04-30T14:30:00Z",
  "readings": {
    "vital_signs": {
      "body_temperature": 38.5,
      "heart_rate": 72,
      "respiratory_rate": 26
    },
    "activity": {
      "steps": 2341,
      "activity_duration_minutes": 285,
      "activity_level": "normal"
    },
    "rumination": {
      "rumination_duration_minutes": 410,
      "rumination_episodes": 8,
      "rumination_quality": "good"
    },
    "behavior": {
      "eating_duration_minutes": 180,
      "lying_duration_minutes": 540,
      "standing_duration_minutes": 300,
      "walking_duration_minutes": 240
    },
    "milk": {
      "milk_yield_liters": 24.5,
      "milk_conductivity": 4.2
    },
    "feeding": {
      "feeding_efficiency_percent": 92.5,
      "feed_intake_estimated": true
    }
  },
  "device_status": {
    "battery_level_percent": 87,
    "signal_strength_percent": 95,
    "gps_accuracy": "high"
  },
  "data_quality": {
    "quality_score": "excellent",
    "data_points_received": 144,
    "data_points_expected": 144
  }
}
```

---

# Sensor Data Fields

## Device Information

| Field              | Type   | Description              |
| ------------------ | ------ | ------------------------ |
| `device_id`        | String | Unique sensor device ID  |
| `device_name`      | String | Device display name      |
| `device_type`      | String | collar / ear_tag         |
| `firmware_version` | String | Current firmware version |

---

## Cattle Information

| Field       | Type   | Description              |
| ----------- | ------ | ------------------------ |
| `rfid_tag`  | String | RFID tag number          |
| `cattle_id` | String | Unique cattle identifier |

---

## Vital Signs

| Field              | Unit | Description      |
| ------------------ | ---- | ---------------- |
| `body_temperature` | °C   | Body temperature |
| `heart_rate`       | BPM  | Heart rate       |
| `respiratory_rate` | RPM  | Respiratory rate |

---

## Activity Monitoring

| Field                       | Description          |
| --------------------------- | -------------------- |
| `steps`                     | Total movement steps |
| `activity_duration_minutes` | Active duration      |
| `activity_level`            | low / normal / high  |

---

## Rumination Monitoring

| Field                         | Description                   |
| ----------------------------- | ----------------------------- |
| `rumination_duration_minutes` | Total rumination duration     |
| `rumination_episodes`         | Number of rumination sessions |
| `rumination_quality`          | poor / good / excellent       |

---

## Behavioral Monitoring

| Field                       | Description       |
| --------------------------- | ----------------- |
| `eating_duration_minutes`   | Eating time       |
| `lying_duration_minutes`    | Resting time      |
| `standing_duration_minutes` | Standing duration |
| `walking_duration_minutes`  | Walking duration  |

---

## Milk Monitoring

| Field               | Description             |
| ------------------- | ----------------------- |
| `milk_yield_liters` | Daily milk yield        |
| `milk_conductivity` | Milk conductivity value |

---

## Feeding Metrics

| Field                        | Description      |
| ---------------------------- | ---------------- |
| `feeding_efficiency_percent` | Feed efficiency  |
| `feed_intake_estimated`      | Estimated intake |

---

## Device Status

| Field                     | Description               |
| ------------------------- | ------------------------- |
| `battery_level_percent`   | Sensor battery percentage |
| `signal_strength_percent` | Signal strength           |
| `gps_accuracy`            | low / medium / high       |

---

## Data Quality

| Field                  | Description             |
| ---------------------- | ----------------------- |
| `quality_score`        | poor / good / excellent |
| `data_points_received` | Actual points received  |
| `data_points_expected` | Expected points         |

---

# Sensor API Success Response

```json
{
  "success": true,
  "message": "Sensor data stored successfully"
}
```

---

# Alerts API

## Endpoint

```http
POST /api/hardware/alerts/
```

---

# Alert Payload

```json
{
  "alert_type": "temperature",
  "severity": "warning",
  "title": "Body Temperature Elevation Detected",
  "description": "Cow Bessie's body temperature has been elevated for the past 2 hours",
  "cattle_id": "COW_001",
  "rfid_tag": "RFID_001",
  "measurement": "body_temperature",
  "measured_value": 39.5,
  "expected_range": "37.0-39.5",
  "threshold_exceeded_by": 0.0,
  "created_at": "2026-04-30T14:35:00Z",
  "action_required": true,
  "recommended_action": "Monitor closely. Consider checking for fever or heat stress."
}
```

---

# Alert Severity Levels

| Severity   | Description                  |
| ---------- | ---------------------------- |
| `info`     | Informational                |
| `warning`  | Medium risk                  |
| `critical` | Immediate attention required |

---

# Latest Readings API

## Endpoint

```http
GET /api/hardware/latest-readings/
```

---

# Latest Alerts API

## Endpoint

```http
GET /api/hardware/latest-alerts/
```

---

# SQL Database Tables

## Device Table

Stores:

* Device details
* Firmware versions
* Sensor type

---

## Cattle Table

Stores:

* RFID tags
* Cattle IDs
* Registration info

---

## SensorReading Table

Stores:

* Vital signs
* Activity metrics
* Rumination data
* Milk production
* Device status
* Quality metrics

---

# MongoDB Collections

## Alerts Collection

Stores:

* Temperature alerts
* Heart rate alerts
* Feeding alerts
* AI anomaly alerts
* Device failures

---

# Recommended Sensor Thresholds

| Metric           | Normal Range    |
| ---------------- | --------------- |
| Body Temperature | 37.5°C - 39.3°C |
| Heart Rate       | 48 - 84 BPM     |
| Respiratory Rate | 10 - 30 RPM     |
| Battery Level    | > 20%           |

---

# Example ESP32 HTTP Request

## Arduino Example

```cpp
HTTPClient http;

http.begin("http://YOUR_SERVER/api/hardware/sensor-data/");

http.addHeader("Content-Type", "application/json");

http.addHeader("X-API-KEY", "super-secret-api-key");

int responseCode = http.POST(jsonPayload);
```

---

# Security Recommendations

* Use HTTPS
* Use API keys
* Rotate API keys periodically
* Validate device IDs
* Add JWT authentication
* Use rate limiting
* Enable logging
* Monitor failed requests

---

# Future Enhancements

* MQTT Integration
* AWS IoT Core
* Firebase Sync
* Real-time WebSockets
* AI Health Prediction
* GPS Tracking
* OTA Firmware Updates
* Device Heartbeat Monitoring
* Edge AI Processing
* Offline Sync
* Redis Queues
* Celery Workers
* Push Notifications
* SMS Alerts
* Telegram Integration
* Multi-farm Management

---

# Recommended Production Stack

| Component      | Technology            |
| -------------- | --------------------- |
| Backend        | Django                |
| API            | Django REST Framework |
| SQL Database   | PostgreSQL            |
| NoSQL Database | MongoDB               |
| Cache          | Redis                 |
| Queue          | Celery                |
| Realtime       | WebSockets            |
| Deployment     | Docker + Nginx        |
| Cloud          | AWS / Azure / GCP     |

---

# License

CattleCare Hardware Sensor System

MIT License

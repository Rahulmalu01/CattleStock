import requests
import random
import time
from datetime import datetime

API_URL = \
"http://127.0.0.1:8000/api/sensor-data/"

API_KEY = \
"cattlecare_hardware_api_2026_secure_key"

while True:

    payload = {

        "device": {
            "device_id": "RFID_001",
            "device_name": "Simulator",
            "device_type": "collar",
            "firmware_version": "1.0"
        },

        "cattle": {
            "cattle_id": "COW_001",
            "rfid_tag": "RFID_001"
        },

        "timestamp":
            datetime.utcnow().isoformat(),

        "readings": {

            "vital_signs": {

                "body_temperature":
                    round(
                        random.uniform(
                            37.5,
                            40.5
                        ),
                        2
                    ),

                "heart_rate":
                    random.randint(
                        60,
                        90
                    ),

                "respiratory_rate":
                    random.randint(
                        20,
                        35
                    )
            },

            "activity": {

                "steps":
                    random.randint(
                        1000,
                        5000
                    ),

                "activity_duration_minutes":
                    random.randint(
                        100,
                        400
                    ),

                "activity_level":
                    random.choice(
                        [
                            "low",
                            "normal",
                            "high"
                        ]
                    )
            }
        },

        "device_status": {

            "battery_level_percent":
                random.randint(
                    20,
                    100
                ),

            "signal_strength_percent":
                random.randint(
                    50,
                    100
                ),

            "gps_accuracy":
                "high"
        }
    }

    r = requests.post(
        API_URL,
        json=payload,
        headers={
            "X-API-KEY":
            API_KEY
        }
    )

    print(
        "Sent:",
        r.status_code
    )

    time.sleep(30)
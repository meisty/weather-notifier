# Weather Notifier ☀️❄️

A lightweight, Raspberry Pi 5-powered Python application that fetches daily weather, pollen, and UV forecasts — and sends customized alerts directly to a Discord channel.

---

## ✨ Features

- **Daily Weather Reports**  
  Fetches and sends daily forecast summaries based on your configured postcode.

- **Data Logging**  
  - Forecast and current weather conditions are stored in a local SQLite database.
  - Supports future analysis, such as comparing forecasted vs actual weather.

- **Customizable**  
  - Configuration via YAML (`config/config.yaml`)
  - Supports multiple alert thresholds.
  - Easy setup for scheduled runs using `cron` or `systemd`.

- **Modular and Extensible**  
  - Organized under `src/` with separate modules for config loading, weather retrieval, database operations, and messaging.

---

## 🚧 Coming soon

**Real-time Health Alerts**  
- Rain chance thresholds
- High or low temperature warnings
- High pollen levels
- Elevated UV index



## 📦 Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/meisty/weather-notifier.git
    cd weather-notifier
    ```

2. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## 🛠️ Usage

Run manually:

```bash
python3 src/main.py
```

Or schedule it with cron to get automatic updates:

```bash
0 7 * * * /usr/bin/python3 /path/to/weather-notifier/src/main.py
```

## ✅ Testing (Planned)

Tests will be added under tests/ using pytest to validate:

- Config loading
- Weather fetching and parsing
- Database insertions
- Alert logic

## 🚀 Future Improvements

- Add test coverage.
- Historical analysis (e.g., comparing forecast vs actual temperatures).
- More detailed Discord summaries.
- Extend health alerts (e.g., air quality).
- Improve error handling and resiliency.

## 📄 License

This project is licensed under the MIT License.
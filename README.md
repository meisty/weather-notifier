# Weather Notifier ☀️🌧️❄️

A command-line Python application running on a Raspberry Pi 5 that provides daily weather updates and health-related alerts (rain, temperature, pollen, UV) directly to a Discord channel.

---

## 🧠 Features

- Fetches daily weather information based on a postcode set in a config file.
- Sends a **once-a-day summary** to Discord with forecast and health alerts.
- Triggers **real-time alerts** if:
  - Rain chance exceeds a configured threshold.
  - Temperature exceeds max or drops below min.
  - Pollen levels are high.
  - UV index is high.
- Simple CLI interface for manual or automated use (via cron or systemd).
- Configurable via YAML.

---

## More information

This is a work in progress, more information will be added in the future

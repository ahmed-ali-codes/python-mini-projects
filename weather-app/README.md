# Python Weather App

A command-line weather application built in Python. This project demonstrates how to make HTTP requests, handle JSON data, and interact with web APIs.

## Features

- **Interactive CLI:** Prompt the user to enter a city.
- **Live Data:** Fetches real-time weather data from the OpenWeatherMap API.
- **JSON Parsing:** Extracts and displays temperature and current weather conditions.
- **Robust Error Handling:** Gracefully handles invalid city names, missing API keys, and network connection issues.

## Concepts Covered

- Web APIs integration
- HTTP Requests (GET) using the `requests` module
- JSON parsing and data extraction
- Exception handling with `try-except` blocks

## Requirements

- Python 3.x
- `requests` library

## Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/weather-app.git
   cd weather-app
   ```

2. **Install dependencies:**
   Make sure you have the `requests` library installed. You can install it using pip:
   ```bash
   pip install requests
   ```

3. **Get an API Key:**
   - Go to [OpenWeatherMap](https://openweathermap.org/) and create a free account.
   - Navigate to your profile to generate a free API key.
   - Open `weather.py` and replace `"YOUR_API_KEY_HERE"` with your actual API key.

## Usage

Run the script from your terminal:

```bash
python weather.py
```

Enter the name of a city when prompted to get the current weather conditions. Type `quit` to exit the application.

### Example Output
```text
Welcome to the Python Weather App!
Enter a city name (or 'quit' to exit): London

--- Weather in London ---
Conditions:  Scattered clouds
Temperature: 15.2°C
-------------------------
```

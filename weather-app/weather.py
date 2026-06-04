import requests
import sys

# Get your free API key from https://openweathermap.org/
API_KEY = "YOUR_API_KEY_HERE"
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

def get_weather(city):
    if API_KEY == "YOUR_API_KEY_HERE":
        print("Error: Please set your OpenWeatherMap API key in weather.py")
        sys.exit(1)

    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric" # Use "imperial" for Fahrenheit
    }
    
    try:
        # Make the HTTP request
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status() # Raise an exception for bad status codes
        
        # Parse the JSON response
        data = response.json()
        
        # Extract the required information
        city_name = data["name"]
        weather_description = data["weather"][0]["description"]
        temperature = data["main"]["temp"]
        
        # Display the results
        print(f"\n--- Weather in {city_name} ---")
        print(f"Conditions:  {weather_description.capitalize()}")
        print(f"Temperature: {temperature}°C")
        print("-" * 25 + "\n")
        
    except requests.exceptions.HTTPError as http_err:
        if response.status_code == 404:
            print(f"\nError: City '{city}' not found. Please check the spelling.\n")
        elif response.status_code == 401:
            print("\nError: Invalid API key. Please check your OpenWeatherMap key.\n")
        else:
            print(f"\nHTTP error occurred: {http_err}\n")
    except requests.exceptions.RequestException as req_err:
        print(f"\nError fetching data: {req_err}\n")
    except KeyError:
        print("\nError: Unexpected data format received from the API.\n")

def main():
    print("Welcome to the Python Weather App!")
    while True:
        city = input("Enter a city name (or 'quit' to exit): ").strip()
        
        if city.lower() == 'quit':
            print("Goodbye!")
            break
        
        if not city:
            print("Please enter a valid city name.")
            continue
            
        get_weather(city)

if __name__ == "__main__":
    main()

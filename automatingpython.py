import requests
import sys

def get_weather(city, api_key):
    # Base URL for WeatherAPI.com Current weather API
    base_url = "http://api.weatherapi.com/v1/current.json"
    
    # Define parameters for the API request
    # 'q' is the query (city name), 'key' is your provided API key
    params = {
        'key': api_key,
        'q': city,
        'aqi': 'no'
    }
    
    try:
        # Make the GET request to the API
        response = requests.get(base_url, params=params)
        
        # Raise an exception if the request returned an unsuccessful status code (e.g., 4xx or 5xx)
        response.raise_for_status()
        
        # Parse the JSON response
        data = response.json()
        
        # Extract location and current weather metrics
        location_name = data['location']['name']
        region = data['location']['region']
        country = data['location']['country']
        
        current = data['current']
        temp_c = current['temp_c']        # Temperature in Celsius
        temp_f = current['temp_f']        # Temperature in Fahrenheit
        humidity = current['humidity']    # Humidity percentage
        wind_kph = current['wind_kph']    # Wind speed in km/h
        wind_mph = current['wind_mph']    # Wind speed in mph
        condition = current['condition']['text'] # Weather condition text
        
        # Print the formatted weather information
        print(f"\nWeather report for {location_name}, {region}, {country}:")
        print(f"Condition:    {condition}")
        print(f"Temperature:  {temp_c}°C ({temp_f}°F)")
        print(f"Humidity:     {humidity}%")
        print(f"Wind Speed:   {wind_kph} km/h ({wind_mph} mph)")
        
    except requests.exceptions.HTTPError as http_err:
        if response.status_code == 400:
            print(f"Error: City '{city}' not found or invalid request parameters.")
        elif response.status_code == 403:
            print("Error: Invalid API Key or disabled service tier.")
        else:
            print(f"HTTP error occurred: {http_err}")
    except requests.exceptions.ConnectionError:
        print("Error: Failed to connect to the server. Check your internet connection.")
    except requests.exceptions.Timeout:
        print("Error: The request timed out.")
    except requests.exceptions.RequestException as req_err:
        print(f"An error occurred: {req_err}")
    except KeyError:
        print("Error: Could not parse the weather data. The API response structure might have changed.")

if __name__ == "__main__":
    # Your provided API Key
    API_KEY = "bf43706b40b84e3babc04008262905"
    
    # Prompt user for a city name or accept it as a command line argument
    if len(sys.argv) > 1:
        city_name = " ".join(sys.argv[1:])
    else:
        city_name = input("Enter the name of a city: ").strip()
        
    if city_name:
        get_weather(city_name, API_KEY)
    else:
        print("City name cannot be empty.")
        
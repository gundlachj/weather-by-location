import requests
import pandas
from datetime import datetime

API_KEY = "78bbc3e46addc45b426224befee59a6c"

LOCATION_LIMIT = 5

def get_location_from_user():
  city_name = input("Enter a city name: ")
  while (city_name.strip() == ""):
    city_name = input("Try again. Enter a city name: ")

  state_code = input("Enter a state code (press Enter to skip): ")
  country_code = input("Enter a country code (press Enter to skip): ")

  return city_name, state_code, country_code

def get_location_info():
  city_name, state_code, country_code = get_location_from_user()
  response = requests.get(f"http://api.openweathermap.org/geo/1.0/direct?q={city_name},{state_code},{country_code}&limit={LOCATION_LIMIT}&appid={API_KEY}")
  while (len(response.json()) == 0):
    print("No locations found. Try again.")
    city_name, state_code, country_code = get_location_from_user()
    response = requests.get(f"http://api.openweathermap.org/geo/1.0/direct?q={city_name},{state_code},{country_code}&limit={LOCATION_LIMIT}&appid={API_KEY}")

  print()

  lon = 0
  lat = 0
  if (len(response.json()) == 1):
    location_data = response.json()[0]
    lon = location_data["lon"]
    lat = location_data["lat"]
  else:
    print("Which city do you want?")
    locations = list()
    index = 0
    for location_json in response.json():
      index += 1
      locations.append(location_json)
      location_info = location_json["name"] + " " + location_json["country"] + " " + location_json["state"]
      print(str(index) + ") " + location_info)

    location_idx_str = input("Which location would you like? ")
    while (location_idx_str.strip() == "" or not location_idx_str.isdigit() or not (int(location_idx_str) > 0 and int(location_idx_str) < len(locations))):
      location_idx_str = input("Try again. Which location would you like? ")

    location_idx = int(location_idx_str)
    
    location_data = locations.pop(location_idx - 1)
    lon = location_data["lon"]
    lat = location_data["lat"]

  return lon, lat

def check_data_exists(data, key):
  if (key in data):
    return data[key]
  else:
    return "ERROR"

def check_time_exists(data, key):
  if (key in data):
    return str(datetime.fromtimestamp(data[key]))
  else:
    return "ERROR"

def get_weather_data(lon, lat):
  response = requests.get(f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}")
  response_dict = response.json()

  weather_data = {}

  weather_data["Description"] = check_data_exists(response_dict["weather"][0], "description")
  weather_data["Temperature"] = check_data_exists(response_dict["main"], "temp")
  weather_data["Feels Like"] = check_data_exists(response_dict["main"], "feels_like")
  weather_data["Min Temp"] = check_data_exists(response_dict["main"], "temp_min")
  weather_data["Max Temp"] = check_data_exists(response_dict["main"], "temp_max")
  weather_data["Pressure"] = check_data_exists(response_dict["main"], "pressure")
  weather_data["Humidity"] = check_data_exists(response_dict["main"], "humidity")
  weather_data["Sea Level Altitude"] = check_data_exists(response_dict["main"], "sea_level")
  weather_data["Ground Level Altitude"] = check_data_exists(response_dict["main"], "grnd_level")
  weather_data["Visibility"] = check_data_exists(response_dict, "visibility")
  weather_data["Wind Speed"] = check_data_exists(response_dict["wind"], "speed")
  weather_data["Wind Deg"] = check_data_exists(response_dict["wind"], "deg")
  weather_data["Wind Gust"] = check_data_exists(response_dict["wind"], "gust")
  weather_data["Current Time"] = check_time_exists(response_dict, "dt")
  weather_data["Sunrise Time"] = check_time_exists(response_dict["sys"], "sunrise")
  weather_data["Sunset Time"] = check_time_exists(response_dict["sys"], "sunset")

  df = pandas.DataFrame.from_dict(weather_data, orient="index", columns=[response_dict["name"]])
  print(df)
  return df

def make_spreadsheet(df):
  df.to_excel("weather-data.xlsx")


def main():
  lon, lat = get_location_info()
  print()
  df = get_weather_data(lon, lat)
  make_spreadsheet(df)

if __name__ == "__main__":
  main()
import requests
import pandas
import openpyxl

# TODO: Replace with secret token
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


def main():
  lon, lat = get_location_info()
  print(lon, lat)

if __name__ == "__main__":
  main()
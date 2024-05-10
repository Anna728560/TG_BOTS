import requests
from config import API_KEY, BASE_URL, LANGUAGE


def get_weather(city):
    try:
        url = f"{BASE_URL}?key={API_KEY}&q={city}&lang={LANGUAGE}&units=metric"
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()

            country_name = data["location"]["country"]
            city_name = data["location"]["name"]
            temp_c = data["current"]["temp_c"]
            feels_like_c = data["current"]["feelslike_c"]
            temp_f = data["current"]["temp_f"]
            feels_like_f = data["current"]["feelslike_f"]

            print(f"City: {city_name},\n"
                  f"Country: {country_name},\n"
                  f"Temperature C: {temp_c}, (feels like: {feels_like_c}),\n"
                  f"Temperature F: {temp_f}, (feels like: {feels_like_f}).\n")

    except Exception as error:
        print(error)
        print("Couldn't get weather. Check your city name.")


def main():
    city = input("Enter your city name: ")
    get_weather(city)


if __name__ == "__main__":
    main()

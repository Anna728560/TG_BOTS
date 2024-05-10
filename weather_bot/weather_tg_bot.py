import requests
import asyncio
import logging
import sys
import os

from datetime import datetime
from math import ceil
from dotenv import load_dotenv

from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import Message

from weather_bot.config import BASE_URL, LANGUAGE, WEATHER_CONDITION


load_dotenv()

TG_TOKEN = os.getenv("TG_TOKEN")
API_KEY = os.getenv("API_KEY")

dp = Dispatcher()


def get_metres_per_second(kph):
    """
    Convert kilometers per hour to meters per second.
    """
    return ceil(kph * (1000/3600))


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """
    This handler receives messages with `/start` command
    """
    await message.answer("Hi! I'm your friendly Asynchronous Weather Bot! 🌦️\n"
                         "Just drop me the name of the city and I'll get you the weather report! 😎")


@dp.message()
async def get_weather(message: Message):
    """
    Handler function to fetch weather information based on user's input city.
    """
    try:
        url = f"{BASE_URL}?key={API_KEY}&q={message.text}&lang={LANGUAGE}&units=metric"
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()

            country_name = data["location"]["country"]
            city_name = data["location"]["name"]
            localtime = data["location"]["localtime"]
            weather_description = data["current"]["condition"]["text"]
            temp_c = data["current"]["temp_c"]
            feels_like_c = data["current"]["feelslike_c"]
            temp_f = data["current"]["temp_f"]
            feels_like_f = data["current"]["feelslike_f"]
            wind_speed = get_metres_per_second(data["current"]["wind_kph"])
            humidity = data["current"]["humidity"]

            await message.answer("Here is the weather for your city...")
            await message.reply(
                f"***{datetime.now().strftime("%Y-%m-%d %H:%M")}***,\n\n"
                f"Country/City: {country_name},{city_name}\n"
                f"Localtime: {localtime},\n\n"
                f"Weather condition: {WEATHER_CONDITION.get(weather_description, weather_description)},\n"
                f"🌡 Temperature C: {temp_c}, (feels like: {feels_like_c}),\n"
                f"🌡 Temperature F: {temp_f}, (feels like: {feels_like_f}),\n\n"
                f"Wind Speed: {wind_speed} metres per second,\n"
                f"Humidity: {humidity},\n\n"
                f"😃 Have a Great Day!\n"
            )
        else:
            await message.reply("Couldn't get weather 🫠\nPlease enter a valid city name in English.")

    except Exception:
        await message.reply("Something went wrong ☹️\nPlease try again.\n")


async def main() -> None:
    bot = Bot(token=TG_TOKEN)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())

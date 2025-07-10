from utils.stock import Stock
from requests import get


API_URL = "https://growagarden.gg/api"
STOCK_URL = f"{API_URL}/stock"
WEATHER_URL = f"{API_URL}/weather"


async def fetch_stock() -> Stock:
    stock = get(STOCK_URL).json()
    return Stock(stock)


async def fetch_weather() -> list[dict]:
    weather = get(WEATHER_URL).json()
    return [weather[item]["name"] for item in weather if weather[item]["timeStarted"]]

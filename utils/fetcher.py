from utils.stock import Stock
from requests import get


# API_URL = "https://growagarden.gg/api"
API_URL = "http://127.0.0.1:3000/api"
STOCK_URL = f"{API_URL}/stock"
WEATHER_URL = f"{API_URL}/weather"


async def fetch_stock() -> Stock:
    stock = get(STOCK_URL).json()
    return Stock(stock)


async def fetch_weather() -> set[str]:
    weather = get(WEATHER_URL).json()
    return {event["displayName"] for event in weather["events"] if event["isActive"] == True}

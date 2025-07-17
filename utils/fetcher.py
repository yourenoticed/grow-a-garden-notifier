from utils.stock import Stock
from requests import get


API_URL = "https://api.joshlei.com/v2/growagarden"
STOCK_URL = f"{API_URL}/stock"
WEATHER_URL = f"{API_URL}/weather"


async def fetch_stock() -> Stock:
    stock = get(STOCK_URL).json()
    return Stock(stock)


async def fetch_weather() -> set[str]:
    weather = get(WEATHER_URL).json()
    return {event["weather_name"] for event in weather["weather"] if event["active"] == True}

from utils.stock import Stock
from requests import get
from requests import JSONDecodeError

API_URL = "https://api.joshlei.com/v2/growagarden"
STOCK_URL = f"{API_URL}/stock"
WEATHER_URL = f"{API_URL}/weather"
INFO_URL = f"{API_URL}/info"


async def fetch_stock() -> Stock:
    try:
        stock = get(STOCK_URL).json()
        return Stock(stock)
    except:
        return Stock(dict())


async def fetch_weather() -> dict:
    try:
        return get(WEATHER_URL).json()
    except JSONDecodeError:
        return dict()

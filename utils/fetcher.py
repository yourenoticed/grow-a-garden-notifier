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


async def fetch_weather() -> set[str]:
    try:
        return get(WEATHER_URL).json()
    except JSONDecodeError:
        return set()


async def fetch_all_items() -> dict:
    all_items = dict()
    try:
        info = get(INFO_URL).json()
        all_items["seeds"] = get_shop_items(info, "seed")
        all_items["gears"] = get_shop_items(info, "gear")
        all_items["eggs"] = get_shop_items(info, "egg")
        all_items["cosmetics"] = get_shop_items(info, "cosmetic")
        all_items["weather"] = get_shop_items(info, "weather")
    finally:
        return all_items


def get_shop_items(info: dict, shop_name: str) -> list[dict]:
    return [{"name": item["display_name"], "rarity": item["rarity"]} for item in info if item["type"] == shop_name]

from utils.db_handler import add_user, get_stock_config, get_weather_config, write_stock_config, write_weather_config, get_user_ids, block_user, unblock_user, get_all_items
from utils.fetcher import fetch_stock, fetch_weather
from utils.stock import Stock


class Service():
    def __init__():
        pass

    async def get_all_weather() -> list[str]:
        weather = await fetch_weather()
        return [event["weather_name"] for event in weather["weather"]]

    async def get_weather_kb(user_id: int) -> list[str]:
        config = Service.get_weather_config(user_id)
        all_weather = await Service.get_all_weather()
        user_kb = list()
        for weather in all_weather:
            user_kb.append(Service._build_btn(weather, config))
        return user_kb

    async def get_stock() -> Stock:
        return await fetch_stock()

    async def get_weather() -> set[str]:
        weather = await fetch_weather()
        return {event["weather_name"] for event in weather["weather"] if event["active"] == True}

    def get_all_items() -> dict:
        return get_all_items()

    async def get_stock_kb(user_id: int, stock_name: str) -> list[str]:
        config = Service.get_stock_config(user_id)
        all_items = Service.get_all_items()
        stock_kb = list()
        for item in all_items[stock_name]:
            stock_kb.append(Service._build_btn(item, config))
        return stock_kb

    def _build_btn(button_text: str, config: list | set) -> str:
        text_builder = [button_text]
        if button_text in config:
            text_builder.append("✅")
        else:
            text_builder.append("❌")
        return " ".join(text_builder)

    def get_weather_config(user_id: int) -> list[str]:
        return get_weather_config(user_id)

    def get_ids() -> list[int]:
        return get_user_ids()

    def get_stock_config(user_id: int) -> list[str]:
        return get_stock_config(user_id)

    def add_user_to_db(user_id: int) -> None:
        return add_user(user_id)

    def write_stock_config_to_db(user_id: int, config: list) -> None:
        return write_stock_config(user_id, config)

    def write_weather_config_to_db(user_id: int, config: list) -> None:
        return write_weather_config(user_id, config)

    def block_user(user_id: int):
        return block_user(user_id)

    def unblock_user(user_id: int):
        return unblock_user(user_id)

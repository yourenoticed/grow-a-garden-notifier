from utils.db_handler import add_user, get_user_config, write_config, get_user_ids, block_user, unblock_user
from utils.fetcher import fetch_stock, fetch_weather
from utils.stock import Stock


class Service():
    def __init__():
        pass

    async def get_stock() -> Stock:
        return await fetch_stock()

    async def get_weather() -> list[dict]:
        return await fetch_weather()

    def get_ids() -> list[int]:
        return get_user_ids()

    def get_config(user_id: int) -> list[str]:
        return get_user_config(user_id)

    def add_user_to_db(user_id: int) -> None:
        return add_user(user_id)

    def write_config_to_db(user_id: int, config: list) -> None:
        return write_config(user_id, config)

    def block_user(user_id: int):
        return block_user(user_id)

    def unblock_user(user_id: int):
        return unblock_user(user_id)

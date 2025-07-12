from aiogram import Bot
from utils.service import Service
from utils.stock import Stock


def build_message(params: dict) -> str:
    message = ["New items in stock!"]
    for shop in params:
        if len(params[shop]) > 0:
            message.append(f"{shop}:\n{params[shop]}")

    if len(message) > 1:
        return "\n\n".join(message)
    else:
        return "The stock has been refreshed but there are no items you need"


async def send_notifications(bot: Bot, stock: Stock, include_eggs=False, include_night=False, include_event=False, include_merchant=False, include_easter=False) -> None:
    chat_ids = Service.get_ids()
    for chat_id in chat_ids:
        config = set(Service.get_config(chat_id))
        message = build_message(stock.__repr__(config))
        if message != "The stock has been refreshed but there are no items you need":
            await Bot.send_message(bot, chat_id, message)


async def send_weather(bot: Bot, weather: list, started=False) -> None:
    chat_ids = Service.get_ids()
    if started == True:
        message = ["New weather!\n"]
        message.extend(weather)
    else:
        message = ["Weather stopped:\n"]
        message.extend(weather)
    text = "\n".join(message)
    for chat_id in chat_ids:
        await Bot.send_message(bot, chat_id, text)

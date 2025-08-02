from aiogram import Bot
from utils.service import Service
from utils.stock import Stock
from handlers.keyboards import main_kb


def build_message(stock_text: str) -> str:
    if len(stock_text) > 0:
        return f"New items in stock!\n\n{stock_text}"
    else:
        return "The stock has been refreshed but there are no items you need"


async def send_notifications(bot: Bot, updates: Stock) -> None:
    chat_ids = Service.get_ids()
    for chat_id in chat_ids:
        config = set(Service.get_stock_config(chat_id))
        stock_text = updates.__str__(config)
        message = build_message(stock_text)
        if message != "The stock has been refreshed but there are no items you need":
            await send_message(bot, chat_id, message)


async def send_weather(bot: Bot, new_weather: set, old_weather: set) -> None:
    chat_ids = Service.get_ids()
    for chat_id in chat_ids:
        message = list()
        weather_config = set(Service.get_weather_config(chat_id))
        started = weather_config.intersection(
            new_weather.difference(old_weather))
        stopped = weather_config.intersection(
            old_weather.difference(new_weather))
        if len(started) > 0:
            started_text = "\n".join(started)
            message.append(f"New weather:\n{started_text}")
        if len(stopped) > 0:
            stopped_text = "\n".join(stopped)
            message.append(f"Weather stopped:\n{stopped_text}")
        if len(message) > 0:
            text = "\n\n".join(message)
            await send_message(bot, chat_id, text)


async def send_message(bot: Bot, chat_id: int, text: str) -> None:
    try:
        await Bot.send_message(bot, chat_id, text, request_timeout=10, reply_markup=main_kb)
    except:
        pass

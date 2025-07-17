from aiogram import Bot
from utils.service import Service
from utils.stock import Stock


def build_message(stock_text: str) -> str:
    if len(stock_text) > 0:
        return f"New items in stock!\n\n{stock_text}"
    else:
        return "The stock has been refreshed but there are no items you need"


async def send_notifications(bot: Bot, stock: Stock, include_eggs=False, include_cosmetics=False, updates=Stock({})) -> None:
    chat_ids = Service.get_ids()
    for chat_id in chat_ids:
        config = set(Service.get_config(chat_id))
        if updates.length() > 0:
            stock_text = updates.__str__(
                config, include_eggs=True, include_cosmetics=True)
        else:
            stock_text = stock.__str__(config, include_cosmetics, include_eggs)
        message = build_message(stock_text)
        if message != "The stock has been refreshed but there are no items you need":
            await send_message(bot, chat_id, message)


async def send_weather(bot: Bot, weather: set, started=False) -> None:
    chat_ids = Service.get_ids()
    weather = list(weather)
    if started == True:
        message = ["New weather!\n"]
        message.extend(weather)
    else:
        message = ["Weather stopped:\n"]
        message.extend(weather)
    text = "\n".join(message)
    for chat_id in chat_ids:
        await send_message(bot, chat_id, text)


async def send_message(bot: Bot, chat_id: int, text: str) -> None:
    try:
        await Bot.send_message(bot, chat_id, text, request_timeout=10)
    except:
        pass

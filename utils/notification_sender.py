from aiogram import Bot
from utils.service import Service
from utils.stock import Stock


def build_message(seeds=str, gears=str, eggs=str) -> str:
    message = ["New items in stock!"]
    if len(seeds) > 0:
        message.append(f"Seeds:\n{seeds}")
    if len(gears) > 0:
        message.append(f"Gears:\n{gears}")
    if len(eggs) > 0:
        message.append(f"Eggs:\n{eggs}")

    if len(message) > 1:
        return "\n\n".join(message)
    else:
        return "The stock has been refreshed but there are no items you need"


async def send_notifications(bot: Bot, stock: Stock, include_eggs=False) -> None:
    chat_ids = Service.get_ids()
    for chat_id in chat_ids:
        config = set(Service.get_config(chat_id))
        seeds_to_send = stock.get_items(stock.seed_shop, config)
        gears_to_send = stock.get_items(stock.gear_shop, config)
        eggs_to_send = ""
        if include_eggs == True:
            eggs_to_send = stock.get_items(stock.egg_shop, config)

        message = build_message(seeds=seeds_to_send,
                                gears=gears_to_send, eggs=eggs_to_send)
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

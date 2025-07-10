from aiogram import Bot
from utils.service import Service
from utils.stock import Stock


def build_message(stock: Stock, seeds=set(), gears=set(), eggs=set()) -> str:
    message = ["New items in stock!"]
    if len(seeds) > 0:
        seeds_list = stock.get_items(stock.seed_shop, seeds)
        message.extend(["\nSeeds:", seeds_list])
    if len(gears) > 0:
        gears_list = stock.get_items(stock.gear_shop, gears)
        message.extend(["\nGears:", gears_list])
    if len(eggs) > 0:
        eggs = "\n".join(eggs)
        message.extend(["\nEggs:", eggs])

    if len(message) > 1:
        return "\n".join(message)
    else:
        return "The stock has been refreshed but there are no items you need"


async def send_notifications(bot: Bot, stock: Stock, include_eggs=False) -> None:
    chat_ids = Service.get_ids()
    for chat_id in chat_ids:
        config = set(Service.get_config(chat_id))
        if include_eggs == True:
            eggs = {item["name"] for item in stock.egg_shop}
            eggs_to_send = eggs.intersection(config)
        seeds = {item["name"] for item in stock.seed_shop}
        gears = {item["name"] for item in stock.gear_shop}
        seeds_to_send = seeds.intersection(config)
        gears_to_send = gears.intersection(config)

        message = build_message(
            stock, seeds=seeds_to_send, gears=gears_to_send, eggs=eggs_to_send)
        if message != "The stock has been refreshed but there are no items you need":
            await Bot.send_message(bot, chat_id, message, reply_markup=None)


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

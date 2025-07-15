from aiogram import Bot
from time import sleep, localtime
from asyncio import run
from utils.notification_sender import send_notifications, send_weather
from utils.service import Service
from utils.stock import Stock
from bot import bot


async def start_polling(bot: Bot) -> None:
    stock, weather = await on_startup(bot)
    while True:
        try:
            weather = await check_weather_updates(bot, weather)
            stock = await check_updates(bot, stock)
            sleep(10)
        except KeyboardInterrupt:
            return


async def on_startup(bot: Bot) -> Stock:
    stock: Stock = await Service.get_stock()
    weather = await Service.get_weather()
    await send_notifications(bot, stock, include_cosmetics=True, include_easter=True, include_eggs=True, include_honey=True, include_night=True)
    await send_weather(bot, weather)
    return (stock, weather)


async def check_updates(bot: Bot, last_stock: Stock) -> Stock:
    new_stock: Stock = await Service.get_stock()
    upd = new_stock.check_update(last_stock)
    match upd:
        case "stock":
            sleep(60)
            new_stock = await Service.get_stock()
            await send_notifications(bot, new_stock)
        case "eggs":
            sleep(60)
            new_stock = await Service.get_stock()
            await send_notifications(bot, new_stock, include_eggs=True,
                                     include_easter=True, include_honey=True, include_night=True)
        case "cosmetics":
            sleep(60)
            new_stock = await Service.get_stock()
            await send_notifications(bot, new_stock, include_eggs=True, include_easter=True,
                                     include_honey=True, include_night=True, include_cosmetics=True)
        case "none":
            update = Stock(new_stock.find_diff(last_stock))
            if update.length() > 0:
                await send_notifications(bot, new_stock, updates=update)
    return new_stock


async def check_weather_updates(bot: Bot, old_weather: set) -> set:
    new_weather: set = await Service.get_weather()
    if len(new_weather) > len(old_weather):
        await send_weather(bot, new_weather.intersection(old_weather), started=True)
    elif len(new_weather) < len(old_weather):
        await send_weather(bot, old_weather.intersection(new_weather), started=False)
    return new_weather


if __name__ == "__main__":
    run(start_polling(bot))

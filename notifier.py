from aiogram import Bot
from time import sleep, localtime
from asyncio import run
from utils.notification_sender import send_notifications, send_weather
from utils.service import Service
from utils.stock import Stock
from bot import bot


async def start_polling(bot: Bot) -> None:
    last_eggs, weather = await on_startup(bot)
    while True:
        try:
            sleep(60)
            # weather = await check_weather_updates(bot, weather)
            last_eggs = await check_updates(bot, last_eggs)
        except KeyboardInterrupt:
            return


async def on_startup(bot: Bot) -> tuple[list]:
    stock: Stock = await Service.get_stock()
    last_eggs = stock.egg_shop
    weather = await Service.get_weather()
    await send_notifications(bot, stock, include_eggs=True)
    return (last_eggs, weather)


async def check_updates(bot: Bot, last_eggs: list) -> list:
    minutes_now = localtime().tm_min
    if minutes_now % 5 == 0:
        sleep(60)
        stock: Stock = await Service.get_stock()
        if minutes_now % 30 == 0 or stock.egg_shop != last_eggs:
            await send_notifications(bot, stock, include_eggs=True)
            return stock.egg_shop
        else:
            await send_notifications(bot, stock, include_eggs=False)
            return last_eggs


async def check_weather_updates(bot: Bot, old_weather: list) -> list:
    new_weather = await Service.get_weather()
    if len(new_weather) != len(old_weather):
        if len(new_weather) > 0:
            await send_weather(bot, new_weather, started=True)
        elif len(new_weather) == 0:
            await send_weather(bot, old_weather, started=False)
        return new_weather
    return old_weather


if __name__ == "__main__":
    run(start_polling(bot))

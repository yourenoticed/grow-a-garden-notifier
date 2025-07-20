from aiogram import Bot
from asyncio import run, sleep
from utils.notification_sender import send_notifications, send_weather
from utils.service import Service
from utils.stock import Stock
from bot import bot


async def start_polling(bot: Bot) -> None:
    stock, weather = await on_startup(bot)
    while True:
        try:
            sleep(10)
            weather = await check_weather_updates(bot, weather)
            stock = await check_updates(bot, stock)
        except KeyboardInterrupt:
            return


async def on_startup(bot: Bot) -> Stock:
    stock: Stock = await Service.get_stock()
    weather = await Service.get_weather()
    await send_notifications(bot, stock)
    await send_weather(bot, new_weather=weather, old_weather=set())
    return (stock, weather)


async def check_updates(bot: Bot, last_stock: Stock) -> Stock:
    new_stock: Stock = await Service.get_stock()
    upd = new_stock.check_update(last_stock)
    await send_notifications(bot, updates=Stock(upd))
    return new_stock


async def check_weather_updates(bot: Bot, old_weather: set) -> set:
    new_weather: set = await Service.get_weather()
    if old_weather != new_weather:
        await send_weather(bot, new_weather=new_weather, old_weather=old_weather)
    return new_weather


if __name__ == "__main__":
    run(start_polling(bot))

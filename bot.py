from config import BOT_TOKEN
from asyncio import run
from aiogram import Bot, Dispatcher
from handlers.handlers import router

bot = Bot(BOT_TOKEN)
dp = Dispatcher()
dp.include_routers(router)


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        run(main())
    except KeyboardInterrupt:
        print("The bot has been stopped manually")

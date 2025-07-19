from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart
from utils.service import Service
from handlers.keyboards import main_kb, weather_kb

router = Router()


@router.message(CommandStart())
async def welcome_message(message: Message):
    Service.add_user_to_db(message.chat.id)
    await show_config(message)


@router.message(F.text == "Stock")
async def show_stock(message: Message):
    stock = await Service.get_stock()
    await message.answer(stock.__str__(include_eggs=True, include_cosmetics=True), reply_markup=main_kb)


@router.message(F.text == "Stock config")
async def show_config(message: Message):
    config = Service.get_stock_config(message.chat.id)
    text = f"Your config:\n{"\n".join(config)}"
    await message.answer(text, reply_markup=main_kb)


@router.message(F.text == "Weather config")
async def start_setup(message: Message):
    weather_setup_kb = await weather_kb(message.chat.id)
    await message.answer(text="Weather config setup:", reply_markup=weather_setup_kb)


@router.message(F.text == "Weather")
async def show_weather(message: Message):
    weather = await Service.get_weather()
    if len(weather) > 0:
        text = f"Current weather:\n{"\n".join(weather)}"
    else:
        text = "There are no weather events right now"
    await message.answer(text, reply_markup=main_kb)


@router.callback_query(F.data.startswith("weather"))
async def add_weather_to_config(callback: CallbackQuery):
    weather = callback.data.split("_")[1]  # getting weather name
    user_config: list = Service.get_weather_config(callback.from_user.id)
    if weather not in user_config:
        user_config.append(weather)
        await callback.message.answer(f"You will receive notifications about {weather}")
    else:
        user_config.remove(weather)
        await callback.message.answer(f"You will stop receiving notifications about {weather}")
    Service.write_weather_config_to_db(callback.from_user.id, user_config)
    weather_setup_kb = await weather_kb(callback.from_user.id)
    await callback.message.edit_reply_markup(reply_markup=weather_setup_kb)


@router.message()
async def add_item_to_config(message: Message):
    user_config: list = Service.get_stock_config(message.chat.id)
    if message.text not in user_config:
        user_config.append(message.text)
        await message.reply("This item has been added to your config")
    else:
        user_config.remove(message.text)
        await message.reply("This item has been removed from your config")
    Service.write_stock_config_to_db(message.chat.id, user_config)

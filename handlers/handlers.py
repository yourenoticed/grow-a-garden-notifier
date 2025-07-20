from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart
from utils.service import Service
from handlers.keyboards import main_kb, weather_kb, stock_kb, get_kb, other_kb

router = Router()


@router.message(CommandStart())
async def welcome_message(message: Message):
    Service.add_user_to_db(message.chat.id)
    await message.answer("Welcome to the GAG stock notifier!", reply_markup=main_kb)


@router.message(F.text == "Stock")
async def show_stock(message: Message):
    stock = await Service.get_stock()
    await message.answer(stock.__str__(include_eggs=True, include_cosmetics=True), reply_markup=main_kb)


@router.message(F.text == "Configs")
async def show_config(message: Message):
    await message.answer(text="Your configs:", reply_markup=stock_kb)


@router.message(F.text == "Weather")
async def show_weather(message: Message):
    weather = await Service.get_weather()
    if len(weather) > 0:
        text = f"Current weather:\n{"\n".join(weather)}"
    else:
        text = "There are no weather events right now"
    await message.answer(text, reply_markup=main_kb)


@router.callback_query(F.data == "configs")
async def return_to_configs(callback: CallbackQuery):
    await callback.message.edit_text(text="Your configs:", reply_markup=stock_kb)


@router.callback_query(F.data.startswith("config"))
async def get_shop_config(callback: CallbackQuery):
    shop_name = callback.data.split("_")[1]
    user_id = callback.from_user.id
    if shop_name == "eggs":
        adjust = 1
    else:
        adjust = 2
    shop_kb = await get_kb(user_id, shop_name, adjust)
    await callback.message.edit_text(f"{shop_name.capitalize()}:", reply_markup=shop_kb)


@router.callback_query(F.data == "weather")
async def start_setup(callback: CallbackQuery):
    weather_setup_kb = await weather_kb(callback.from_user.id)
    await callback.message.edit_text(text="Weather:", reply_markup=weather_setup_kb)


@router.callback_query(F.data.startswith("weather"))
async def add_weather_to_config(callback: CallbackQuery):
    weather_name = callback.data.split("_")[1]  # getting weather name
    user_id = callback.from_user.id
    user_config: list = Service.get_weather_config(user_id)
    if weather_name not in user_config:
        user_config.append(weather_name)
    else:
        user_config.remove(weather_name)
    Service.write_weather_config_to_db(user_id, user_config)
    weather_setup_kb = await weather_kb(user_id)
    await callback.message.edit_reply_markup(reply_markup=weather_setup_kb)


@router.callback_query(F.data.startswith("stock"))
async def add_item_to_config(callback: CallbackQuery):
    data = callback.data.split("_")
    shop_name = data[1]
    item_name = data[2]
    user_id = callback.from_user.id
    user_config: list = Service.get_stock_config(user_id)
    if item_name not in user_config:
        user_config.append(item_name)
    else:
        user_config.remove(item_name)
    Service.write_stock_config_to_db(user_id, user_config)
    if shop_name == "eggs":
        adjust = 1
    else:
        adjust = 2
    shop_setup_kb = await get_kb(user_id, shop_name, adjust)
    await callback.message.edit_reply_markup(reply_markup=shop_setup_kb)


@router.callback_query(F.data == "other")
async def other_configs(callback: CallbackQuery):
    setting_kb = await other_kb(callback.from_user.id)
    await callback.message.edit_text(text="Other configs:", reply_markup=setting_kb)


@router.callback_query(F.data.startswith("setting"))
async def add_setting_to_config(callback: CallbackQuery):
    setting_name = callback.data.split("_")[1]
    user_id = callback.from_user.id
    user_config: list = Service.get_stock_config(user_id)
    if setting_name not in user_config:
        user_config.append(setting_name)
    else:
        user_config.remove(setting_name)
    Service.write_stock_config_to_db(user_id, user_config)
    setting_kb = await other_kb(user_id)
    await callback.message.edit_reply_markup(reply_markup=setting_kb)


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

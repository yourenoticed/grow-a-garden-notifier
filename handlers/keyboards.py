from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from utils.service import Service

main_kb = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="Stock"), KeyboardButton(text="Weather")],
                                        [KeyboardButton(text="Stock config")],
                                        [KeyboardButton(text="Weather config")]],
                              resize_keyboard=True)


async def weather_kb(chat_id: int) -> InlineKeyboardMarkup:
    weather_kb_builder = InlineKeyboardBuilder()
    user_kb: list[str] = await Service.get_weather_kb(chat_id)
    for button_text in user_kb:
        btn_name = button_text.split()[0]
        weather_kb_builder.button(
            text=button_text, callback_data=f"weather_{btn_name}")
    return weather_kb_builder.adjust(2).as_markup()

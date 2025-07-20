from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from utils.service import Service

main_kb = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="Stock"), KeyboardButton(text="Weather")],
                                        [KeyboardButton(text="Configs")]],
                              resize_keyboard=True)

stock_kb = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Seeds", callback_data="config_seeds")],
                                                 [InlineKeyboardButton(
                                                     text="Gears", callback_data="config_gears")],
                                                 [InlineKeyboardButton(
                                                     text="Eggs", callback_data="config_eggs")],
                                                 [InlineKeyboardButton(
                                                     text="Weather", callback_data="weather")],
                                                 [InlineKeyboardButton(text="Other", callback_data="other")]])


async def weather_kb(chat_id: int) -> InlineKeyboardMarkup:
    weather_kb_builder = InlineKeyboardBuilder()
    weather_kb_texts: list[str] = await Service.get_weather_kb(chat_id)
    for button_text in weather_kb_texts:
        btn_name = button_text.split()[0]
        weather_kb_builder.button(
            text=button_text, callback_data=f"weather_{btn_name}")
    weather_markup = weather_kb_builder.adjust(2).as_markup()
    return_to_stock_btn(weather_markup)
    return weather_markup


async def get_kb(chat_id: int, shop_name: str, adjust=2) -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()
    kb_texts: list[str] = await Service.get_stock_kb(chat_id, shop_name)
    for button_text in kb_texts:
        btn_name = " ".join(button_text.split()[:-1])
        kb_builder.button(text=button_text,
                          callback_data=f"stock_{shop_name}_{btn_name}")
    kb_markup = kb_builder.adjust(adjust).as_markup()
    return_to_stock_btn(kb_markup)
    return kb_markup


async def other_kb(chat_id: int) -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()
    kb_texts: list[str] = await Service.get_other_kb(chat_id)
    for button_text in kb_texts:
        btn_name = " ".join(button_text.split()[:-1])
        kb_builder.button(text=button_text,
                          callback_data=f"setting_{btn_name}")
    kb_markup = kb_builder.adjust(1).as_markup()
    return_to_stock_btn(kb_markup)
    return kb_markup


def return_to_stock_btn(markup: InlineKeyboardMarkup) -> None:
    markup.inline_keyboard.append([InlineKeyboardButton(
        text="Back", callback_data="configs")])

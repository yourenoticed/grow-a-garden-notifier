from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


main_kb = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="Stock")],
                                        [KeyboardButton(text="Config")]], resize_keyboard=True)

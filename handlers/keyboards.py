from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


main_kb = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="Stock")],
                                        [KeyboardButton(text="Config")],
                                        [KeyboardButton(text="Weather")]],
                              resize_keyboard=True)

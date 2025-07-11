from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import CommandStart
from utils.service import Service
from handlers.keyboards import main_kb

router = Router()


@router.message(CommandStart())
async def welcome_message(message: Message):
    Service.add_user_to_db(message.chat.id)
    await show_config(message)


@router.message(F.text == "Stock")
async def show_stock(message: Message):
    stock = await Service.get_stock()
    await message.answer(stock.__str__(), reply_markup=main_kb)


@router.message(F.text == "Config")
async def show_config(message: Message):
    config = Service.get_config(message.chat.id)
    text = f"Your config:\n{"\n".join(config)}"
    await message.answer(text, reply_markup=main_kb)


# @router.chat_member(ChatMemberUpdatedFilter(chat_member_updated.IS_NOT_MEMBER))
# async def on_user_leave(event: ChatMemberUpdated):
#     return Service.block_user(event.chat.id)


# @router.chat_member(ChatMemberUpdatedFilter(chat_member_updated.IS_MEMBER))
# async def on_user_join(event: ChatMemberUpdated):
#     return Service.unblock_user(event.chat.id)


@router.message()
async def add_item_to_config(message: Message):
    user_config: list = Service.get_config(message.chat.id)
    if message.text not in user_config:
        user_config.append(message.text)
        await message.reply("This item has been added to your config")
    else:
        user_config.remove(message.text)
        await message.reply("This item has been removed from your config")
    Service.write_config_to_db(message.chat.id, user_config)

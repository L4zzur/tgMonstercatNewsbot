from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from config import config
from filters import IsAdmin
from keyboards import inline

router = Router()


@router.message(CommandStart(), IsAdmin(config.ADMIN_IDS))
async def start(message: Message) -> None:
    await message.answer(
        "Добро пожаловать в бота для создания новостных постов.",
        reply_markup=inline.new_post_kb(),
    )


@router.message(CommandStart(), ~IsAdmin(config.ADMIN_IDS))
async def not_start(message: Message) -> None:
    await message.answer("Nothing there.")

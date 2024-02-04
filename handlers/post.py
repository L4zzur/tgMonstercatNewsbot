from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message

from config import config
from filters import IsAdmin
from keyboards import inline
from scrapper import MonstercatNews
from utils import states

router = Router()


@router.message(states.Post.new_post, IsAdmin(config.ADMIN_IDS))
async def create_post(
    message: Message,
    state: FSMContext,
) -> None:
    await state.clear()
    if not message.text:
        await message.answer("Неправильно введена ссылка или дата")
        return
    try:
        url, date = message.text.split()
    except ValueError:
        await message.answer("Неправильно введена ссылка или дата")
        return
    try:
        news = MonstercatNews(url, date)
    except ValueError:
        await message.answer("Неправильно введена ссылка или дата")
        return

    image_url = news.get_image_url()
    text = news.get_post_text()

    await message.answer_photo(image_url, caption=text)

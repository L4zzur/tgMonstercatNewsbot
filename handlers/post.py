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


@router.callback_query(F.data == "new_post", IsAdmin(config.ADMIN_IDS))
async def new_post(callback: CallbackQuery, state: FSMContext) -> None:
    await callback.message.edit_text(  # type: ignore
        "Прикрепите presave ссылку на релиз и дату выхода через пробел.\nНапример: monster.cat/sorcererssymphony 7.02.2024",
        disable_web_page_preview=True,
    )

    await state.set_state(states.Post.new_post)


@router.message(states.Post.new_post, IsAdmin(config.ADMIN_IDS))
async def create_post(
    message: Message,
    state: FSMContext,
) -> None:
    await state.clear()
    if not message.text:
        await message.answer("Неправильно введена ссылка или дата")
        return
    url, date = message.text.split()
    try:
        news = MonstercatNews(url, date)
    except ValueError:
        await message.answer("Неправильно введена ссылка или дата")
        return

    image_url = news.get_image_url()
    text = news.get_post_text()

    await message.answer_photo(image_url, caption=text)

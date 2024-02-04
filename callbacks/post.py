from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from config import config
from filters import IsAdmin
from utils import states

router = Router()


@router.callback_query(F.data == "new_post", IsAdmin(config.ADMIN_IDS))
async def new_post(callback: CallbackQuery, state: FSMContext) -> None:
    await callback.message.edit_text(  # type: ignore
        "Прикрепите presave ссылку на релиз и дату выхода через пробел.\nНапример: monster.cat/sorcererssymphony 7.02.2024",
        disable_web_page_preview=True,
    )

    await state.set_state(states.Post.new_post)

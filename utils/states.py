from aiogram.fsm.state import State, StatesGroup


class Post(StatesGroup):
    new_post = State()

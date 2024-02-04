from aiogram import Router


def setup_callback_routers() -> Router:
    from . import post

    router = Router()
    router.include_router(post.router)
    return router

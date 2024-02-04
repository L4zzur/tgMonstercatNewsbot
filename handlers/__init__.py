from aiogram import Router


def setup_message_routers() -> Router:
    from . import post, start

    router = Router()
    router.include_router(start.router)
    router.include_router(post.router)
    return router

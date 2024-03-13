__all__ = ("router",)

from aiogram import Router

from src.routers.router import router as command_router

router = Router(name=__name__)

router.include_routers(
    command_router,
)

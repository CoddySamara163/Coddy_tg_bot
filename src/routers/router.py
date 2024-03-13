from pathlib import Path

from aiogram import Router, types, F
from aiogram.filters import CommandStart
from aiogram.utils.chat_action import ChatActionSender
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from src.settings import settings
from src.routers.messages import (
    START_MESSAGE,
    CALLBACK_MESSAGE,
    END_MESSAGE,
    RESPONSE_MESSAGE,
)

router = Router(name=__name__)


class Context(StatesGroup):
    age_category = State()


@router.message(CommandStart())
async def handle_start(message: types.Message) -> None:
    print(message.chat.id)
    async with ChatActionSender.typing(bot=message.bot, chat_id=message.chat.id):
        await message.answer_photo(
            photo=types.FSInputFile(
                str(
                    Path(__file__).parent.parent
                    / "static"
                    / "photo_2024-02-26_20-41-30.jpg"
                ),
                filename="coddy_lesson",
            )
        )
    builder = InlineKeyboardBuilder()
    builder.button(text="7-10 лет", callback_data="7-10 лет")
    builder.button(text="11-15 лет", callback_data="11-15 лет")
    builder.adjust(1)
    await message.answer(
        text=START_MESSAGE,
        reply_markup=builder.as_markup(),
    )


@router.callback_query(F.data.in_(("7-10 лет", "11-15 лет")))
async def handle_age(callback_query: types.CallbackQuery, state: FSMContext) -> None:
    await state.set_state(Context.age_category)
    await state.update_data(age_category=callback_query.data)
    builder = ReplyKeyboardBuilder()
    builder.button(text="Номер телефона", request_contact=True)
    # builder.adjust(1)
    # await callback_query.message.answer(
    #     text=CALLBACK_MESSAGE, reply_markup=builder.as_markup(resize_keyboard=True)
    # )
    await callback_query.bot.send_message(
        chat_id=callback_query.from_user.id,
        text=CALLBACK_MESSAGE,
        reply_markup=builder.as_markup(resize_keyboard=True),
    )


@router.message(F.contact)
async def handle_contact(message: types.Message, state: FSMContext):
    age_category = await state.get_data()
    await message.answer(
        END_MESSAGE,
        reply_markup=types.ReplyKeyboardRemove(),
    )

    await message.bot.send_message(
        chat_id=settings.RESPONSE_CHAT_ID,
        text=RESPONSE_MESSAGE.format(
            full_name=message.from_user.full_name,
            username=message.from_user.username,
            phone_number=message.contact.phone_number,
            age_category=age_category.get("age_category"),
        ),
    )

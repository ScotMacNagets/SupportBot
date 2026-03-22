from aiogram import Router
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import Admin
from core.text import AdminRegister
from fsm.admin_registration import Registration
from services import key_repo

router = Router()

async def _admin_register_helper(
        username: str,
        telegram_id: int,
        session: AsyncSession,
) -> Admin:
    admin = Admin(
        username=username,
        telegram_id=telegram_id,
    )
    session.add(admin)
    await session.commit()
    await session.refresh(admin)
    return admin


@router.message(Command("register"))
async def admin_register(
        message: Message,
        state: FSMContext,
        session: AsyncSession,
):
    #Начало регистрации, просим ввести уникальный ключ
    await state.set_state(Registration.input_key)
    await message.answer(
        text="Введите уникальный ключ для регистрации"
    )

@router.message(Registration.input_key)
async def admin_register_check_key(
        message: Message,
        state: FSMContext,
        session: AsyncSession,
):
    #Проверяем ключ
    check_key = await key_repo.check_key(
        session=session,
        input_key=message.text,
    )

    if check_key:
        await state.clear()
        #заполняем данные админа
        username = message.from_user.username
        telegram_id = message.from_user.id
        await _admin_register_helper(
            username=username,
            telegram_id=telegram_id,
            session=session,
        )
        await message.answer(
            text=AdminRegister.SUCCESSFUL_REGISTRATION.format(
                username=username,
                telegram_id=telegram_id,
            ),
        )

        return
    await message.answer(
        text="⚠️ Не удалось вас зарегестрировать.\n\n"
        "Обратитесь к <a href='https://t.me/{admin_username}'>администратору</a> " 
        "для получения доступа.",
        parse_mode=ParseMode.HTML,
    )


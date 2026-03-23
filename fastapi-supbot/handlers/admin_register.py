import logging

from aiogram import Router
from aiogram.enums import ParseMode
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext

from aiogram.types import Message
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from core.config import settings
from core.models import Admin
from core.text import AdminRegister
from fsm.admin_registration import Registration
from services import key_repo

logger = logging.getLogger(__name__)

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
):
    #Начало регистрации, просим ввести уникальный ключ
    await state.set_state(Registration.input_key)
    await message.answer(
        text=AdminRegister.INPUT_REGISTER_KEY,
        parse_mode=ParseMode.HTML,
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
        try:
            await _admin_register_helper(
                username=username,
                telegram_id=telegram_id,
                session=session,
            )
        except IntegrityError as e:
            logger.info("Unsuccessful registration: admin already registered, %s", e)
            await message.answer(
                text=AdminRegister.ALREADY_REGISTERED
            )
            return
        logger.info("Successful registration: %s", username)
        await message.answer(
            text=AdminRegister.SUCCESSFUL_REGISTRATION.format(
                username=username,
                telegram_id=telegram_id,
            ),
        )

        return
    logger.warning("Unsuccessful registration: %s", message.from_user.username)
    await message.answer(
        text=AdminRegister.UNSUCCESSFUL_REGISTRATION.format(
            username=settings.superuser.username,
        ),
        parse_mode=ParseMode.HTML,
    )


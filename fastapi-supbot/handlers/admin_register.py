from aiogram import Router
from aiogram.filters import Command

from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import db_helper, Admin

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
        session: AsyncSession,
):
    username = message.from_user.username
    telegram_id = message.from_user.id
    await _admin_register_helper(
        username=username,
        telegram_id=telegram_id,
        session=session,
    )
    await message.answer(
        text=f"Вы успешно зарегестрированы\n\n username: {username}\ntelegram_id: {telegram_id}",
    )

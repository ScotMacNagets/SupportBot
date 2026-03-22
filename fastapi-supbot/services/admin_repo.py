from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import Admin


async def get_all_admins(session: AsyncSession):
    query = select(Admin).where(
        Admin.current_chat_id == None,
    ).order_by(Admin.id)
    admins = await session.execute(query)
    return admins

async def get_admin(session: AsyncSession, telegram_id: int):
    query = select(Admin).where(
        Admin.telegram_id == telegram_id,
    )
    result = await session.execute(query)
    admin = result.scalar_one_or_none()
    if admin:
        return admin
    return None

async def get_admin_before_delete(session: AsyncSession, telegram_id: int):
    query = select(Admin).where(
        Admin.telegram_id == telegram_id,
        Admin.current_chat_id == None,
    )
    result = await session.execute(query)
    admin = result.scalar_one_or_none()
    if admin:
        return admin
    return None

async def superuser_check(session: AsyncSession, telegram_id: int):
    query = select(Admin).where(
        Admin.is_superuser == True,
        Admin.telegram_id == telegram_id,
    )
    result = await session.execute(query)
    admin = result.scalar_one_or_none()
    if admin:
        return True
    return False

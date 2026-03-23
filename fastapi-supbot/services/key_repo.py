import secrets
import string
import bcrypt
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.models.key import Key


def _generate_key():
    alphabet = string.ascii_letters + string.digits
    raw_key = "".join(secrets.choice(alphabet) for _ in range(32))

    hashed = bcrypt.hashpw(raw_key.encode(), bcrypt.gensalt())

    return raw_key, hashed.decode("utf-8")

async def generate_new_key(session: AsyncSession):
    key_obj = await get_latest_key(session=session)
    if key_obj:
        raw_key, hashed_key = _generate_key()
        key_obj.hashed_key = hashed_key

        await session.commit()
        await session.refresh(key_obj)

        return raw_key
    return None

async def get_latest_key(session: AsyncSession):
    query = select(Key).where(
        Key.id == 1,
    )
    result = await session.execute(query)
    key = result.scalar_one_or_none()
    return key

async def check_key(session: AsyncSession, input_key: str):
    key_obj = await get_latest_key(session=session)

    if not key_obj:
        return False

    return bcrypt.checkpw(
        input_key.encode(),
        key_obj.hashed_key.encode("utf-8")
    )


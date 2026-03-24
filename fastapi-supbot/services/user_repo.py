import secrets
import string

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import User


class UserRepository:
    def __init__(
            self,
            session: AsyncSession
    ):
        self.session = session

    async def get_user(self, user_id: int) -> User | None:
        query = select(User).where(
            User.external_id == user_id,
        )
        result = await self.session.execute(query)
        user = result.scalar_one_or_none()
        if user:
            return user
        return None

    async def create_user(self, user_id: str) -> User:
        user = User(
            external_id=user_id,
        )
        self.session.add(user)
        await self.session.commit()

        return user
from typing import Optional, List

from sqlalchemy import or_, select, and_

from app.user.models import User
from app.user.schemas.user import LoginResponseSchema
from core.db import Transactional, session
from core.exceptions import (
    PasswordDoesNotMatchException,
    DuplicateEmailOrNicknameException,
    UserNotFoundException,
)
from core.utils.token_helper import TokenHelper


class UserService:
    def __init__(self):
        ...

    async def get_user_list(
        self,
        limit: int = 12,
        prev: Optional[int] = None,
    ) -> List[User]:
        query = select(User)

        # if prev:
        #     query = query.where(User.Id < prev)

        if limit > 12:
            limit = 12

        query = query.limit(limit)
        result = await session.execute(query)
        return result.scalars().all()

    @Transactional()
    async def create_user(
        self, email: str, password1: str, password2: str, nickname: str
    ) -> None:
        if password1 != password2:
            raise PasswordDoesNotMatchException

        query = select(User).where(or_(User.Email == email, User.NickName == nickname))
        result = await session.execute(query)
        is_exist = result.scalars().first()
        if is_exist:
            raise DuplicateEmailOrNicknameException

        user = User(Email=email, Password=password1, NickName=nickname)
        session.add(user)

    async def is_admin(self, user_id: int) -> bool:
        result = await session.execute(select(User).where(User.Id == user_id))
        print("is_admin pass")
        user = result.scalars().first()
        if not user:
            return False

        if user.IsAdmin is False:
            return False

        return True

    async def login(self, email: str, password: str) -> LoginResponseSchema:
        result = await session.execute(
            select(User).where(and_(User.Email == email, password == password))
        )
        user = result.scalars().first()
        if not user:
            raise UserNotFoundException
        response = LoginResponseSchema(
            token=TokenHelper.encode(payload={"user_id": user.Id}),
            refresh_token=TokenHelper.encode(payload={"sub": "refresh"}),
        )
        return response

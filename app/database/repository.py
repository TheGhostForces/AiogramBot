import asyncio
from sqlalchemy import select, update
from app.database.database import new_session
from app.database.models import TrustedUsersOrm, HistoryOrm, UsersOrm


class VerifyUser:
    @classmethod
    async def verification_user(cls, id_telegram: int, username: str, secret_key: str):
        async with new_session() as session:
            result = await session.execute(
                select(TrustedUsersOrm)
                .where(TrustedUsersOrm.id_telegram_account == id_telegram)
                .where(TrustedUsersOrm.username == username)
                .where(TrustedUsersOrm.secret_key == secret_key)
            )
            return result.scalar_one_or_none()

    # @classmethod
    # async def add(cls):
    #     async with new_session() as session:
    #         new_user = TrustedUsersOrm(
    #             id_telegram_account=your_id,
    #             username='your_telegram_username',
    #             secret_key='your_secret_key'
    #         )
    #         session.add(new_user)
    #         await session.commit()

    @classmethod
    async def get_path(cls, id_telegram: int, username: str):
        async with new_session() as session:
            result = await session.execute(
                select(TrustedUsersOrm.file_path)
                .where(TrustedUsersOrm.id_telegram_account == id_telegram)
                .where(TrustedUsersOrm.username == username)
            )
            return result.scalar()

    @classmethod
    async def update_path(cls, id_telegram: int, username: str, file_path: str):
        async with new_session() as session:
            await session.execute(
                update(TrustedUsersOrm)
                .where(TrustedUsersOrm.id_telegram_account == id_telegram)
                .where(TrustedUsersOrm.username == username)
                .values(file_path=file_path)
            )
            await session.commit()

class Users:
    @classmethod
    async def add_user(cls, id_telegram: int, username: str, attempts: int):
        async with new_session() as session:
            new_user = UsersOrm(
                id_telegram_account=id_telegram,
                username=username,
                attempts=attempts
            )
            session.add(new_user)
            await session.commit()

    @classmethod
    async def check_user(cls, id_telegram: int, username: str):
        async with new_session() as session:
            result = await session.execute(
                select(UsersOrm)
                .where(UsersOrm.id_telegram_account == id_telegram)
                .where(UsersOrm.username == username)
            )
            return result.scalar_one_or_none()

    @classmethod
    async def check_user_attempts(cls, id_telegram: int, username: str):
        async with new_session() as session:
            result = await session.execute(
                select(UsersOrm.attempts)
                .where(UsersOrm.id_telegram_account == id_telegram)
                .where(UsersOrm.username == username)
            )
            return result.scalar()

    @classmethod
    async def update_attempts(cls, id_telegram: int, username: str, attempts: int):
        async with new_session() as session:
            await session.execute(
                update(UsersOrm)
                .where(UsersOrm.id_telegram_account == id_telegram)
                .where(UsersOrm.username == username)
                .values(attempts=attempts)
            )
            await session.commit()

class History:
    @classmethod
    async def add_log(cls, action: str, success: bool, id_telegram: int, username: str):
        async with new_session() as session:
            new_log = HistoryOrm(
                action=action,
                success=success,
                id_telegram_account=id_telegram,
                username=username,
            )
        session.add(new_log)
        await session.commit()

# if __name__ == "__main__":
#     asyncio.run(VerifyUser.add())

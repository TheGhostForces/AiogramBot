from datetime import datetime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Enum as SQLEnum, func, JSON
from app.database.enums import LogsAction


class Model(DeclarativeBase):
    pass


class TrustedUsersOrm(Model):
    __tablename__ = "TrustedUsers"


    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    id_telegram_account: Mapped[int] = mapped_column(nullable=False)
    username: Mapped[str] = mapped_column(nullable=False)
    file_path: Mapped[str] = mapped_column(nullable=True)
    secret_key: Mapped[str] = mapped_column(nullable=False)

class UsersOrm(Model):
    __tablename__ = "Users"


    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    id_telegram_account: Mapped[int] = mapped_column(nullable=False)
    username: Mapped[str] = mapped_column(nullable=False)
    attempts: Mapped[int] = mapped_column(nullable=False)

class HistoryOrm(Model):
    __tablename__ = "History"


    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    action: Mapped[LogsAction] = mapped_column(SQLEnum(LogsAction) ,nullable=False)
    success: Mapped[bool] = mapped_column(nullable=True)
    details: Mapped[dict] = mapped_column(JSON, nullable=True)
    id_telegram_account: Mapped[int] = mapped_column(nullable=False)
    username: Mapped[str] = mapped_column(nullable=False)
    timestamp: Mapped[datetime] = mapped_column(server_default=func.now(),nullable=False)
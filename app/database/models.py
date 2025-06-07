from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

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
    action: Mapped[str] = mapped_column(nullable=False)
    success: Mapped[bool] = mapped_column(nullable=False)
    id_telegram_account: Mapped[int] = mapped_column(nullable=False)
    username: Mapped[str] = mapped_column(nullable=False)
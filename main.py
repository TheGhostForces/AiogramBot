import asyncio
from app.bot import dp, bot
from app.database.database import create_tables
from app.routers.def_rt import router as def_rt
from app.routers.auth_rt import router as auth_rt
from app.routers.choose_rt import router as choose_rt
from app.routers.file_sys_rt import router as f_s_rt
from app.routers.sys_rt import router as s_rt


async def main():
    await create_tables()
    dp.include_router(auth_rt)
    dp.include_router(choose_rt)
    dp.include_router(f_s_rt)
    dp.include_router(s_rt)
    dp.include_router(def_rt)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
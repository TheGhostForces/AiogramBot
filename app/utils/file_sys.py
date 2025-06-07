import shutil
from pathlib import Path
from app.database.repository import VerifyUser


async def current_directory(message):
    current_path = await VerifyUser.get_path(message.from_user.id, message.from_user.username)
    if not current_path:
        current_path = "C:/"
        await VerifyUser.update_path(message.from_user.id, message.from_user.username, current_path)
    return current_path

async def update_path(message, new_path: str):
    await VerifyUser.update_path(message.from_user.id, message.from_user.username, new_path)

async def get_folder_content(current_path: str) -> dict[int, str]:
    current_path = Path(current_path)
    content = {}

    for index, item in enumerate(sorted(current_path.iterdir()), start=1):
        if item.is_dir():
            content[index] = f"📁 {item.name}"
        else:
            content[index] = f"📄 {item.name}"
    return content

async def delete_content_by_number(current_path: str, content: dict, number: int):
    value = content[number]
    content_path = Path(current_path + value[2:])
    if content_path.exists() and content_path.is_dir():
        shutil.rmtree(content_path)
    if content_path.exists() and content_path.is_file():
        content_path.unlink()
    return content_path

async def change_path_directory(current_path: str, content: dict, number: int):
    if number in content:
        value = content[number]
        new_path = current_path + value[2:]
        np = Path(new_path)
        if np.exists() and np.is_dir():
            return new_path
        if np.exists() and np.is_file():
            return "is_file"
    else:
        return None

async def check_absolute_folder(path: str) -> bool:
    p = Path(path)
    return p.is_absolute() and p.is_dir()

async def check_exists_folder(path: str):
    current_path = Path(path)
    return current_path.exists() and current_path.is_dir()

async def one_level_up(current_path: str) -> str:
    path = Path(current_path.rstrip("/\\"))
    parent = path.parent
    return str(parent)

async def show_content_folder(message):
    try:
        current_path = await current_directory(message)
        content = await get_folder_content(current_path)
        result_text = "\n".join(f"{idx}. {name}" for idx, name in content.items())
        await message.answer(f"Вы находитесь по пути: {current_path}\n\n{result_text}", parse_mode="HTML")
        if not content:
            await message.answer("Папка пуста.")
    except PermissionError:
        await message.answer("Похоже, вы выбрали папку, где вам отказали в доступе, поэтому вы были возвращены в C:/")
        await VerifyUser.update_path(message.from_user.id, message.from_user.username, "C:/")
        content = await get_folder_content("C:/")
        result_text = "\n".join(f"{idx}. {name}" for idx, name in content.items())
        await message.answer(f"Вы находитесь по пути: C:/\n\n{result_text}", parse_mode="HTML")
        if not content:
            await message.answer("Папка пуста.")
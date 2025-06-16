import ctypes
import datetime
import platform
from pathlib import Path
import GPUtil
import psutil
import pyautogui
import subprocess
from aiogram.types import FSInputFile


async def prevent_sleep():
    ctypes.windll.user32.mouse_event(1, 0, 1, 0, 0)
    ctypes.windll.user32.mouse_event(1, 0, -1, 0, 0)

async def get_system_uptime():
    boot_time_timestamp = psutil.boot_time()
    boot_time = datetime.datetime.fromtimestamp(boot_time_timestamp)
    now = datetime.datetime.now()

    uptime = now - boot_time
    return uptime, boot_time.strftime("%d.%m.%Y %H:%M:%S")

async def get_uploading_components():
    cpu_percent = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory()
    gpus = GPUtil.getGPUs()
    partitions = psutil.disk_partitions()
    text = f"🖥 Системная информация:\n"
    text += f"• Загрузка CPU: {cpu_percent}%\n"
    text += f"• ОЗУ: {memory.used / 1024 ** 2:.1f} MB / {memory.total / 1024 ** 2:.1f} MB ({memory.percent}%)\n"

    if gpus:
        for gpu in gpus:
            text += f"\n🎮 GPU: {gpu.name}\n"
            text += f"  • Загрузка: {gpu.load * 100:.1f}%\n"
            text += f"  • Память: {gpu.memoryUsed:.1f} MB / {gpu.memoryTotal:.1f} MB\n"
            text += f"  • Температура: {gpu.temperature} °C\n"
    else:
        text += "\n🎮 GPU не найден\n"

    text += "\n💾 Диски:\n"
    for part in partitions:
        try:
            usage = psutil.disk_usage(part.mountpoint)
            text += f"• {part.device}: {usage.used / 1024 ** 3:.1f} GB / {usage.total / 1024 ** 3:.1f} GB ({usage.percent}%)\n"
        except PermissionError:
            text += f"• {part.device}: ❌ Нет доступа\n"

    return text

async def get_parent_pids():
    all_pids = {p.pid for p in psutil.process_iter()}
    parent_pids = set()

    for proc in psutil.process_iter(['ppid']):
        try:
            ppid = proc.info['ppid']
            if ppid in all_pids:
                parent_pids.add(ppid)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    return parent_pids

async def get_process_list():
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H_%M_%S')
    save_dir = Path("all_processes")
    save_dir.mkdir(parents=True, exist_ok=True)
    filename = save_dir / f"proccess_info_{timestamp}.txt"
    parent_pids = await get_parent_pids()

    with open(filename, "w", encoding="utf-8") as f:
        f.write(f"Главные процессы на {timestamp}\n")
        f.write("=" * 80 + "\n\n")

        for proc in psutil.process_iter(
                ['pid', 'name', 'username', 'status', 'cpu_percent', 'memory_percent', 'create_time']):
            try:
                if proc.pid in parent_pids:
                    info = proc.info
                    f.write(f"PID: {info['pid']}\n")
                    f.write(f"Имя процесса: {info['name']}\n")
                    f.write(f"Пользователь: {info.get('username', 'N/A')}\n")
                    f.write(f"Статус: {info['status']}\n")
                    f.write(f"CPU (%): {info['cpu_percent']}\n")
                    f.write(f"Память (%): {info['memory_percent']:.2f}\n")
                    f.write(
                        f"Время запуска: {datetime.datetime.fromtimestamp(info['create_time']).strftime('%Y-%m-%d %H:%M:%S')}\n")
                    f.write("-" * 80 + "\n")
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                continue
        file = FSInputFile(filename)
        return filename, file

async def screenshot():
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H_%M_%S')
    save_dir = Path("all_screenshots")
    save_dir.mkdir(parents=True, exist_ok=True)
    filename = f'screenshot_{timestamp}.png'
    filepath = Path("all_screenshots") / filename # your folder for screenshots
    screenshot = pyautogui.screenshot()
    screenshot.save(filepath)
    return filepath

async def shutdown_or_restart_pc(mode: str):
    system_os = platform.system()
    if system_os == "Windows":
        if mode == "shutdown":
            subprocess.run(["shutdown", "/s", "/t", "1"])
        elif mode == "restart":
            subprocess.run(["shutdown", "/r", "/t", "1"])
    elif system_os == "Linux" or system_os == "Darwin":
        if mode == "shutdown":
            subprocess.run(["shutdown", "-h", "now"])
        elif mode == "restart":
            subprocess.run(["sudo", "shutdown", "-r", "now"])

async def kill_process_by_pid(pid: int):
    try:
        process = psutil.Process(pid)
        name = process.name()
        process.terminate()
        process.wait(timeout=3)

        if process.is_running():
            process.kill()
        return name, f"Процесс с PID {pid} был мягко завершен"
    except psutil.NoSuchProcess:
        return "Not Found", f"Процесс с PID {pid} не найден."
    except psutil.AccessDenied:
        process = psutil.Process(pid)
        name = process.name()
        return name, f"Нет доступа к завершению процесса с PID {pid}."
import ctypes
import datetime
import platform
import time
from pathlib import Path
import GPUtil
import psutil
import pyautogui
import subprocess


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

async def get_process_list(limit=50):
    process_info = []
    for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_info']):
        try:
            info = proc.info
            mem_mb = info['memory_info'].rss / 1024 / 1024
            process_info.append({
                'name': info['name'],
                'pid': info['pid'],
                'cpu': info['cpu_percent'],
                'mem': round(mem_mb, 2)
            })
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

    process_info.sort(key=lambda x: x['cpu'], reverse=True)

    output = "🖥️ *Топ процессов по CPU:*\n\n"
    for proc in process_info[:limit]:
        output += (
            f"🔹 {proc['name']}\n"
            f"  PID: {proc['pid']}\n"
            f"  CPU: {proc['cpu']}%\n"
            f"  RAM: {proc['mem']} MB\n\n"
        )
    return output

async def screenshot():
    timestamp = time.strftime("%Y%m%d_%H%M%S")
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
import datetime
from pathlib import Path
from app.database.repository import History
import json


async def get_logs_bot_list():
    timestamp = datetime.datetime.now()
    save_dir = Path("all_bot_logs")
    save_dir.mkdir(parents=True, exist_ok=True)
    filename = save_dir / f"selection_from_logs_{timestamp.strftime('%Y-%m-%d %H_%M_%S')}.txt"
    logs = await History.get_all_logs()

    with open(filename, "w", encoding="utf-8") as f:
        for log in logs:
            line = (
                f"ID: {log.id} | Time: {log.timestamp.strftime('%Y-%m-%d %H:%M:%S')} | "
                f"User: {log.username} (ID: {log.id_telegram_account}) | "
                f"Action: {log.action.name} | Success: {log.success} | "
                f"Details: {json.dumps(log.details, ensure_ascii=False)}"
            )
            f.write(line + "\n")

    return timestamp, filename
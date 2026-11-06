
import csv
import time
from datetime import datetime

import psutil

# Вариант №4
INTERVAL = 1
SAMPLES = 40
THRESHOLDS = {"cpu": 60, "ram": 75, "disk": 80}
LOG_FILE = "monitor_log.csv"


def take_sample():
    battery = psutil.sensors_battery()

    return {
        "time": datetime.now().strftime("%H:%M:%S"),
        "cpu": psutil.cpu_percent(interval=None),
        "ram": psutil.virtual_memory().percent,
        "disk": psutil.disk_usage("C:\\").percent,
        "battery": (
            battery.percent if battery is not None else "N/A"
        ),
    }


def check_alerts(sample):
    alerts = []

    for metric, limit in THRESHOLDS.items():
        if sample[metric] >= limit:
            alerts.append(
                f"{metric.upper()} = {sample[metric]}% "
                f"(порог {limit}%)"
            )

    return alerts


def main():
    results = {"cpu": [], "ram": [], "disk": []}

    # Подготовка первого измерения CPU
    psutil.cpu_percent(interval=None)

    with open(LOG_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "time", "cpu", "ram",
                "disk", "battery", "alert"
            ]
        )
        writer.writeheader()

        for i in range(SAMPLES):
            time.sleep(INTERVAL)

            sample = take_sample()
            alerts = check_alerts(sample)

            sample["alert"] = "; ".join(alerts)
            writer.writerow(sample)

            for metric in results:
                results[metric].append(sample[metric])

            warning = (
                " <-- ВНИМАНИЕ: " + sample["alert"]
                if alerts else ""
            )

            print(
                f"{i + 1}/{SAMPLES} "
                f"CPU: {sample['cpu']}% "
                f"RAM: {sample['ram']}% "
                f"DISK: {sample['disk']}% "
                f"BATTERY: {sample['battery']}%"
                f"{warning}"
            )

    print("\n=== СТАТИСТИКА ===")

    for metric, values in results.items():
        avg = sum(values) / len(values)
        maximum = max(values)
        minimum = min(values)

        print(
            f"{metric.upper()}: "
            f"среднее = {avg:.1f}%, "
            f"максимум = {maximum:.1f}%, "
            f"минимум = {minimum:.1f}%"
        )

    print(f"\nЖурнал сохранён в {LOG_FILE}")


if __name__ == "__main__":
    main()

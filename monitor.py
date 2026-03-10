#the main brain chcek the health on aloop

import psutil
import time
import logging
from datetime import datetime
import config
from alert import send_alert

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(config.LOG_FILE),
        logging.StreamHandler()
    ]
)

def check_cpu():
    usage = psutil.cpu_percent(interval=1)
    status = "CRITICAL" if usage > config.CPU_THRESHOLD else "OK"
    logging.info(f"CPU USAGE: {usage}% [{status}]")

    if status == "CRITICAL":
        send_alert(
            subject=f"CPU Critical: {usage}%",
            body=f"CPU reached {usage}%.\nThreshold:{config.CPU_THRESHOLD}%\nTime: {datetime.now()}"

        )
    return usage

def check_memory():
    memory = psutil.virtual_memory()
    usage = memory.percent
    used_gb = round(memory.used /1024/1024/1024, 2)
    total_gb = round(memory.total /1024/ 1024 / 1024, 2)
    status = "CRITICAL" if usage > config.MEMORY_THRESHOLD else "OK"
    logging.info(f"Memory: {usage}% [{status}] - {used_gb}GB of {total_gb}GB used")

    if status == "CRITICAL":
        send_alert(
            subject=f"Memory critical: {usage}%",
            body=f"Memory reached {usage}%.\nThreshold: {config.MEMORY_THERSHOLD}%\nTime: {datetime.now()}"

        )
    return usage

def check_disk():
    disk = psutil.disk_usage('/')
    usage = disk.percent
    used_gb = round(disk.used / 1024 / 1024 / 1024, 2)
    free_gb = round(disk.free / 1024 / 1024 / 1024, 2)
    status = "CRITICAL" if usage > config.DISK_THRESHOLD else "OK"
    logging.info(f"Disk: {usage}% [{status}] — {used_gb}GB used, {free_gb}GB free")

    if status == "CRITICAL":
        send_alert(
            subject=f"Disk Critical: {usage}%",
            body=f"Disk reached {usage}%.\nThreshold: {config.DISK_THRESHOLD}%\nTime: {datetime.now()}"
        )
    return usage
def check_top_processes():
    processes = sorted(
        psutil.process_iter(['pid', 'name', 'cpu_percent']),
        key=lambda p: p.info['cpu_percent'],
        reverse=True
    )[:5]

    logging.info("Top 5 processes by CPU:")
    for proc in processes:
        logging.info(f"  PID {proc.info['pid']} — {proc.info['name']} — {proc.info['cpu_percent']}%")


def run_monitor():
    logging.info("=== Health Monitor Started ===")
    logging.info(f"CPU threshold: {config.CPU_THRESHOLD}% | Memory: {config.MEMORY_THRESHOLD}% | Disk: {config.DISK_THRESHOLD}%")
    logging.info(f"Checking every {config.CHECK_INTERVAL} seconds")

    while True:
        logging.info("--- Running health check ---")
        check_cpu()
        check_memory()
        check_disk()
        check_top_processes()
        logging.info(f"Next check in {config.CHECK_INTERVAL} seconds\n")
        time.sleep(config.CHECK_INTERVAL)


if __name__ == "__main__":
    run_monitor()

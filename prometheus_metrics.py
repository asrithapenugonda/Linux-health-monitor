# prometheus_metrics.py
# Reads from the same psutil data as monitor.py
# but exposes it as a Prometheus endpoint on port 8000

import psutil
import time
import threading
import logging
from prometheus_client import start_http_server, Gauge, Counter
import config

# --- Define metrics ---
CPU_GAUGE    = Gauge("linux_cpu_percent",    "Current CPU usage percent")
MEM_GAUGE    = Gauge("linux_memory_percent", "Current memory usage percent")
DISK_GAUGE   = Gauge("linux_disk_percent",   "Current disk usage percent")
MEM_USED_GB  = Gauge("linux_memory_used_gb", "Memory used in GB")
DISK_FREE_GB = Gauge("linux_disk_free_gb",   "Disk free space in GB")
ALERT_COUNTER = Counter("linux_alerts_total", "Total number of threshold alerts fired", ["metric"])

def collect_and_expose():
    """Collect system metrics and update Prometheus gauges."""
    while True:
        # CPU
        cpu = psutil.cpu_percent(interval=1)
        CPU_GAUGE.set(cpu)
        if cpu > config.CPU_THRESHOLD:
            ALERT_COUNTER.labels(metric="cpu").inc()

        # Memory
        mem = psutil.virtual_memory()
        MEM_GAUGE.set(mem.percent)
        MEM_USED_GB.set(round(mem.used / 1024 / 1024 / 1024, 2))
        if mem.percent > config.MEMORY_THRESHOLD:
            ALERT_COUNTER.labels(metric="memory").inc()

        # Disk
        disk = psutil.disk_usage('/')
        DISK_GAUGE.set(disk.percent)
        DISK_FREE_GB.set(round(disk.free / 1024 / 1024 / 1024, 2))
        if disk.percent > config.DISK_THRESHOLD:
            ALERT_COUNTER.labels(metric="disk").inc()

        logging.info(f"[Prometheus] CPU: {cpu}% | MEM: {mem.percent}% | DISK: {disk.percent}%")
        time.sleep(config.CHECK_INTERVAL)

def start_prometheus_server():
    """Start Prometheus HTTP server and begin collecting metrics."""
    start_http_server(8000)
    logging.info("Prometheus metrics available at http://localhost:8000")
    collect_and_expose()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    print("Starting Prometheus metrics server on http://localhost:8000")
    start_prometheus_server()
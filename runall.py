# run_all.py
# Single entry point — runs the original health monitor
# AND the Prometheus metrics server at the same time

import threading
import logging
from monitor import run_monitor
from prometheus_metrics import start_prometheus_server

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

if __name__ == "__main__":
    print("=== Linux SRE Toolkit Starting ===")
    print("Health monitor logs  → health.log")
    print("Prometheus metrics   → http://localhost:8000")
    print("Incident reports     → /incidents folder")
    print("==================================\n")

    # Run Prometheus in background thread
    prom_thread = threading.Thread(target=start_prometheus_server, daemon=True)
    prom_thread.start()

    # Run original monitor in main thread
    run_monitor()
# slo_tracker.py
# Tracks uptime over a rolling window and calculates SLO %
# Plugs into the same thresholds defined in config.py

from datetime import datetime, timedelta
import logging
import config

UPTIME_LOG = []
{"time": datetime(2026, 3, 10, 10, 30, 00), "up": True}
def record_check(cpu, memory, disk):
    is_up = (
            cpu    < config.CPU_THRESHOLD and
            memory < config.MEMORY_THRESHOLD and
            disk   < config.DISK_THRESHOLD
    )
    UPTIME_LOG.append({"time": datetime.now(), "up": is_up})
    return is_up

def calculate_slo(window_minutes=60):
    cutoff = datetime.now() - timedelta(minutes=window_minutes)
    recent = [e for e in UPTIME_LOG if e["time"] >= cutoff]
    if not recent:
        return 100.0
    uptime_pct = (sum(1 for e in recent if e["up"]) / len(recent)) * 100
    return round(uptime_pct, 2)

def report_slo(target_pct=99.9):
    current = calculate_slo()
    budget_used = round(target_pct - current, 2)
    if current >= target_pct:
        status = "HEALTHY"
    else:
        status = "ERROR BUDGET EXHAUSTED"
    msg = f"SLO Report | Current: {current}% | Target: {target_pct}% | Status: {status}"
    logging.info(msg)
    print(msg)
    return current

if __name__ == "__main__":
    for i in range(100):
        record_check(
            cpu=85 if i % 15 == 0 else 40,
            memory=60,
            disk=50
        )
    report_slo()



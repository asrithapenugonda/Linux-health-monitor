# Linux System Health Monitor

A Python-based SRE toolkit that monitors Linux system health in real time, exposes metrics to Prometheus, tracks SLOs, auto-generates incident reports, and sends email alerts when thresholds are breached.

Built to reflect real Site Reliability Engineering practices — observability, alerting, SLO tracking, and incident documentation all in one lightweight tool.

---

## What it does

- Monitors CPU, memory, and disk usage on a configurable interval
- Sends email alerts the moment any metric exceeds its threshold
- Exposes all metrics as a live Prometheus scrape endpoint on port 8000
- Tracks uptime over a rolling window and calculates SLO percentage against a target
- Auto-generates a structured Markdown incident report every time a threshold is breached
- Logs top 5 CPU-consuming processes on every check
- Runs the health monitor and Prometheus server simultaneously using Python threading

---

## Project Structure

```
linux-health-monitor/
├── run_all.py              # single entry point — starts everything
├── monitor.py              # main health check loop + email alerting
├── prometheus_metrics.py   # Prometheus scrape endpoint on port 8000
├── slo_tracker.py          # SLO calculator with rolling window
├── incident.py             # auto incident report generator
├── config.py               # all thresholds and settings in one place
├── alert.py                # email alert logic via SMTP
├── requirements.txt        # dependencies
└── incidents/              # auto-created — stores incident markdown files
```

---

## Live Prometheus Output

When running, the following custom metrics are available at `http://localhost:8000`:

```
# HELP linux_cpu_percent Current CPU usage percent
# TYPE linux_cpu_percent gauge
linux_cpu_percent 17.0

# HELP linux_memory_percent Current memory usage percent
# TYPE linux_memory_percent gauge
linux_memory_percent 84.9

# HELP linux_disk_percent Current disk usage percent
# TYPE linux_disk_percent gauge
linux_disk_percent 34.7

# HELP linux_memory_used_gb Memory used in GB
# TYPE linux_memory_used_gb gauge
linux_memory_used_gb 6.67

# HELP linux_disk_free_gb Disk free space in GB
# TYPE linux_disk_free_gb gauge
linux_disk_free_gb 253.06

# HELP linux_alerts_total Total number of threshold alerts fired
# TYPE linux_alerts_total counter
linux_alerts_total{metric="cpu"} 3.0
linux_alerts_total{metric="memory"} 1.0
```

---

## Sample Terminal Output

```
=== Linux SRE Toolkit Starting ===
Health monitor logs  → health.log
Prometheus metrics   → http://localhost:8000
Incident reports     → /incidents folder
==================================

2026-03-10 19:18:38,347 - INFO - === Health Monitor Started ===
2026-03-10 19:18:38,347 - INFO - CPU threshold: 80% | Memory: 85% | Disk: 90%
2026-03-10 19:18:38,347 - INFO - Checking every 60 seconds
2026-03-10 19:18:39,364 - INFO - CPU USAGE: 16.9% [OK]
2026-03-10 19:18:39,365 - INFO - Memory: 84.9% [OK] - 6.67GB of 7.85GB used
2026-03-10 19:18:39,365 - INFO - Disk: 34.7% [OK] — 134.52GB used, 253.06GB free
2026-03-10 19:18:39,365 - INFO - [Prometheus] CPU: 17.0% | MEM: 84.9% | DISK: 34.7%
2026-03-10 19:18:39,819 - INFO - Top 5 processes by CPU:
2026-03-10 19:18:39,819 - INFO -   PID 10480 — chrome.exe — 7.6%
2026-03-10 19:18:39,819 - INFO -   PID 20248 — idea64.exe — 6.2%
2026-03-10 19:18:39,819 - INFO - Next check in 60 seconds
```

---

## Auto-Generated Incident Report Example

When a threshold is breached, a report is automatically created in `/incidents`:

```markdown
# Incident Report

| Field         | Detail                         |
|---------------|--------------------------------|
| Metric        | CPU                            |
| Value         | 92%                            |
| Threshold     | 80%                            |
| Time          | 2026-03-10 19:45:02            |
| Detected      | Linux Health Monitor (auto)    |

## What Happened
CPU usage reached 92%, exceeding the configured threshold of 80%.

## Immediate Actions Taken
- Alert email sent to on-call
- Incident report auto-generated
- Metric recorded in Prometheus

## Suggested Next Steps
- [ ] Check which processes are consuming the most CPU
- [ ] Review recent deployments or config changes
- [ ] Check for runaway processes
- [ ] Resolve and update this report with root cause

## Status
- [ ] Investigating
- [ ] Mitigated
- [ ] Resolved
```

---

## How to Run

**1. Clone the repo**
```bash
git clone https://github.com/asrithapenugonda/Linux-health-monitor.git
cd Linux-health-monitor
```

**2. Install dependencies**
```bash
pip install -r requirements.txt
```

**3. Set environment variables for email alerts**
```bash
# Windows
$env:EMAIL_SENDER = "youremail@gmail.com"
$env:EMAIL_PASSWORD = "your-gmail-app-password"

# Linux / Mac
export EMAIL_SENDER="youremail@gmail.com"
export EMAIL_PASSWORD="your-gmail-app-password"
```

**4. Run everything**
```bash
python run_all.py
```

**5. View live Prometheus metrics**

Open your browser and go to:
```
http://localhost:8000
```

---

## Configuration

All thresholds and settings live in `config.py` — change them without touching any logic.

| Setting            | Default | Description                        |
|--------------------|---------|------------------------------------|
| CPU_THRESHOLD      | 80%     | Alert if CPU exceeds this          |
| MEMORY_THRESHOLD   | 85%     | Alert if memory exceeds this       |
| DISK_THRESHOLD     | 90%     | Alert if disk exceeds this         |
| CHECK_INTERVAL     | 60s     | Seconds between each health check  |
| LOG_FILE           | health.log | Where logs are written          |

---

## SLO Tracking

`slo_tracker.py` calculates uptime percentage over a rolling time window. A check is counted as healthy only if all three metrics — CPU, memory, and disk — are below their thresholds simultaneously.

```bash
python slo_tracker.py
```

```
SLO Report | Current: 98.3% | Target: 99.9% | Status: ERROR BUDGET EXHAUSTED
```

The default target is 99.9%. Adjust `window_minutes` to calculate SLO over different periods — 60 minutes, 24 hours, 30 days.

---

## Architecture

```
run_all.py
    │
    ├── Thread 1 (daemon) ──→ prometheus_metrics.py
    │                              reads psutil every 60s
    │                              updates Gauges + Counters
    │                              serves metrics at :8000
    │
    └── Thread 2 (main) ──→ monitor.py
                               reads psutil every 60s
                               checks thresholds
                               sends email alerts
                               logs to health.log
                               triggers incident reports
```

---

## Tech Stack

| Tool                  | Purpose                                      |
|-----------------------|----------------------------------------------|
| Python 3.9            | Core language                                |
| psutil                | System metrics — CPU, memory, disk, processes|
| prometheus-client     | Metrics exposition and Prometheus integration|
| smtplib               | Email alerting via Gmail SMTP                |
| threading             | Concurrent execution of monitor + Prometheus |
| logging               | Structured timestamped log output            |
| os / datetime         | File I/O and incident report generation      |

---

## What I Learned

- How Prometheus scraping works — pull model vs push model, Gauges vs Counters, labels
- SLO and error budget concepts used in production SRE environments
- Python threading — daemon threads, concurrent execution, why target functions are passed without brackets
- Separating configuration from logic using environment variables for secrets
- Post-mortem and incident documentation culture in SRE teams
- Structured logging with timestamps and log levels
- Context managers for safe file I/O
- Building modular Python projects where each file has a single clear responsibility

---

## Roadmap

- [ ] Connect to Grafana for dashboard visualisation
- [ ] Deploy on AWS EC2 and run as a systemd background service
- [ ] Add network latency and packet loss monitoring
- [ ] Add Slack alerting alongside email
- [ ] Containerise with Docker and add a docker-compose.yml

---
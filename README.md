# ⚡ Energy-Efficient CPU Scheduler

A power-aware CPU scheduling simulation using Dynamic Voltage and Frequency Scaling (DVFS) and thermal-aware scheduling.

## Features
- FCFS, Round Robin, and Priority scheduling algorithms
- DVFS controller (Low/Mid/High frequency levels)
- Thermal model simulation
- Live Gantt chart and frequency/temperature graphs
- Algorithm comparison analytics dashboard
- CSV export of results

## Modules
- `scheduler_engine/` — Core scheduling logic and DVFS
- `gui_dashboard/` — Interactive GUI with live charts
- `analytics/` — Algorithm comparator and reporting

## How to Run
```bash
py main.py
```

## Technologies
- Python 3.12
- Tkinter (GUI)
- Matplotlib (Charts)
- Pandas (Data analysis)

## Course
CSE-316 | CA2 Project | LPU 
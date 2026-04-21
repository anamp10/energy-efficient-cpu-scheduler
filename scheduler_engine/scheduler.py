import time
import random

class Task:
    def __init__(self, task_id, burst_time, priority, arrival_time):
        self.task_id = task_id
        self.burst_time = burst_time
        self.priority = priority
        self.arrival_time = arrival_time
        self.remaining_time = burst_time
        self.completion_time = 0
        self.waiting_time = 0
        self.turnaround_time = 0
        self.energy_consumed = 0
        self.frequency = 1.0
        self.voltage = 1.0

def get_dvfs_level(cpu_load):
    if cpu_load < 30:
        return {"freq": 0.6, "voltage": 0.8, "label": "LOW"}
    elif cpu_load < 70:
        return {"freq": 0.8, "voltage": 0.9, "label": "MID"}
    else:
        return {"freq": 1.0, "voltage": 1.0, "label": "HIGH"}

def calculate_energy(voltage, freq, time_units):
    k = 0.5
    return k * (voltage ** 2) * freq * time_units

def calculate_temperature(current_temp, freq, idle=False):
    if idle:
        return max(40, current_temp - 2)
    return min(95, current_temp + (freq * 5))

def fcfs(tasks):
    tasks = sorted(tasks, key=lambda t: t.arrival_time)
    current_time = 0
    temperature = 40
    log = []
    for task in tasks:
        cpu_load = random.randint(50, 90)
        dvfs = get_dvfs_level(cpu_load)
        task.frequency = dvfs["freq"]
        task.voltage = dvfs["voltage"]
        task.energy_consumed = calculate_energy(
            task.voltage, task.frequency, task.burst_time)
        task.waiting_time = max(0, current_time - task.arrival_time)
        current_time += task.burst_time
        task.completion_time = current_time
        task.turnaround_time = task.completion_time - task.arrival_time
        temperature = calculate_temperature(temperature, task.frequency)
        log.append({
            "task_id": task.task_id,
            "start": current_time - task.burst_time,
            "end": current_time,
            "freq": task.frequency,
            "voltage": task.voltage,
            "energy": round(task.energy_consumed, 3),
            "temp": round(temperature, 1),
            "dvfs": dvfs["label"]
        })
    return tasks, log

def round_robin(tasks, quantum=3):
    tasks = sorted(tasks, key=lambda t: t.arrival_time)
    queue = [Task(t.task_id, t.burst_time, t.priority, t.arrival_time)
             for t in tasks]
    current_time = 0
    temperature = 40
    log = []
    completed = []
    while queue:
        task = queue.pop(0)
        cpu_load = random.randint(40, 80)
        dvfs = get_dvfs_level(cpu_load)
        run_time = min(quantum, task.remaining_time)
        task.frequency = dvfs["freq"]
        task.voltage = dvfs["voltage"]
        energy = calculate_energy(task.voltage, task.frequency, run_time)
        task.energy_consumed += energy
        temperature = calculate_temperature(temperature, task.frequency)
        log.append({
            "task_id": task.task_id,
            "start": current_time,
            "end": current_time + run_time,
            "freq": task.frequency,
            "energy": round(energy, 3),
            "temp": round(temperature, 1),
            "dvfs": dvfs["label"]
        })
        current_time += run_time
        task.remaining_time -= run_time
        if task.remaining_time > 0:
            queue.append(task)
        else:
            task.completion_time = current_time
            task.turnaround_time = task.completion_time - task.arrival_time
            task.waiting_time = task.turnaround_time - task.burst_time
            completed.append(task)
    return completed, log

def priority_scheduling(tasks):
    tasks = sorted(tasks, key=lambda t: (t.arrival_time, t.priority))
    current_time = 0
    temperature = 40
    log = []
    for task in tasks:
        cpu_load = 90 if task.priority <= 2 else 50
        dvfs = get_dvfs_level(cpu_load)
        task.frequency = dvfs["freq"]
        task.voltage = dvfs["voltage"]
        task.energy_consumed = calculate_energy(
            task.voltage, task.frequency, task.burst_time)
        task.waiting_time = max(0, current_time - task.arrival_time)
        current_time += task.burst_time
        task.completion_time = current_time
        task.turnaround_time = task.completion_time - task.arrival_time
        temperature = calculate_temperature(temperature, task.frequency)
        log.append({
            "task_id": task.task_id,
            "start": current_time - task.burst_time,
            "end": current_time,
            "freq": task.frequency,
            "voltage": task.voltage,
            "energy": round(task.energy_consumed, 3),
            "temp": round(temperature, 1),
            "dvfs": dvfs["label"]
        })
    return tasks, log
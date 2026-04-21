import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from scheduler_engine.scheduler import Task, fcfs, round_robin, priority_scheduling
import matplotlib.pyplot as plt
import pandas as pd

def generate_test_tasks(n=8):
    import random
    tasks = []
    for i in range(1, n+1):
        tasks.append(Task(i,
            burst_time=random.randint(2, 10),
            priority=random.randint(1, 5),
            arrival_time=random.randint(0, 5)))
    return tasks

def run_all_algorithms(tasks):
    results = {}
    algos = {
        "FCFS": fcfs,
        "Round Robin": round_robin,
        "Priority": priority_scheduling
    }
    for name, algo in algos.items():
        tasks_copy = [Task(t.task_id, t.burst_time, t.priority, t.arrival_time)
                     for t in tasks]
        completed, log = algo(tasks_copy)
        total_energy = sum(t.energy_consumed for t in completed)
        avg_wait = sum(t.waiting_time for t in completed) / len(completed)
        avg_turnaround = sum(t.turnaround_time for t in completed) / len(completed)
        results[name] = {
            "total_energy": round(total_energy, 3),
            "avg_wait": round(avg_wait, 3),
            "avg_turnaround": round(avg_turnaround, 3),
            "throughput": len(completed)
        }
    return results

def show_comparison_charts(results):
    algorithms = list(results.keys())
    energy = [results[a]["total_energy"] for a in algorithms]
    wait = [results[a]["avg_wait"] for a in algorithms]
    turnaround = [results[a]["avg_turnaround"] for a in algorithms]

    colors = ["#a6e3a1", "#89b4fa", "#f38ba8"]

    fig, axes = plt.subplots(1, 3, figsize=(14, 5))
    fig.patch.set_facecolor("#1e1e2e")
    fig.suptitle("Algorithm Comparison", color="#cba6f7",
                fontsize=14, fontweight="bold")

    data = [
        (axes[0], energy, "Total Energy (J)", "Energy Consumption"),
        (axes[1], wait, "Avg Wait Time (ms)", "Average Waiting Time"),
        (axes[2], turnaround, "Avg Turnaround (ms)", "Average Turnaround Time"),
    ]

    for ax, values, ylabel, title in data:
        bars = ax.bar(algorithms, values, color=colors, edgecolor="#1e1e2e", width=0.5)
        ax.set_facecolor("#313244")
        ax.set_title(title, color="#cba6f7", fontsize=11)
        ax.set_ylabel(ylabel, color="#cdd6f4", fontsize=9)
        ax.tick_params(colors="#cdd6f4")
        for spine in ax.spines.values():
            spine.set_edgecolor("#45475a")
        for bar, val in zip(bars, values):
            ax.text(bar.get_x() + bar.get_width()/2,
                   bar.get_height() + 0.1,
                   str(val), ha="center", va="bottom",
                   color="#cdd6f4", fontsize=9, fontweight="bold")

    plt.tight_layout()
    plt.savefig("analytics/comparison_chart.png", dpi=150,
               bbox_inches="tight", facecolor="#1e1e2e")
    plt.show()

def export_csv(results):
    df = pd.DataFrame(results).T
    df.index.name = "Algorithm"
    df.to_csv("analytics/comparison_results.csv")
    print("✅ Results exported to analytics/comparison_results.csv")

def run_comparison():
    print("🔄 Generating test tasks...")
    tasks = generate_test_tasks(8)
    print("⚙️  Running all algorithms...")
    results = run_all_algorithms(tasks)
    print("\n📊 Results:")
    for algo, metrics in results.items():
        print(f"  {algo}: Energy={metrics['total_energy']}J | "
              f"AvgWait={metrics['avg_wait']}ms | "
              f"Turnaround={metrics['avg_turnaround']}ms")
    show_comparison_charts(results)
    export_csv(results)
    return results

if __name__ == "__main__":
    run_comparison()
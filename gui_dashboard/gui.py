import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.patches as mpatches
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from scheduler_engine.scheduler import Task, fcfs, round_robin, priority_scheduling

class CPUSchedulerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Energy-Efficient CPU Scheduler")
        self.root.geometry("1200x750")
        self.root.configure(bg="#1e1e2e")
        self.tasks = []
        self.task_counter = 1
        self.build_ui()

    def build_ui(self):
        # Title
        title = tk.Label(self.root, text="⚡ Energy-Efficient CPU Scheduler",
                        font=("Helvetica", 18, "bold"),
                        bg="#1e1e2e", fg="#cba6f7")
        title.pack(pady=10)

        # Main frame
        main_frame = tk.Frame(self.root, bg="#1e1e2e")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10)

        # Left panel
        left = tk.Frame(main_frame, bg="#313244", width=320)
        left.pack(side=tk.LEFT, fill=tk.Y, padx=(0,10), pady=5)
        left.pack_propagate(False)

        tk.Label(left, text="Add Task", font=("Helvetica", 13, "bold"),
                bg="#313244", fg="#89dceb").pack(pady=(15,5))

        # Input fields
        fields = [("Burst Time (ms):", "burst"),
                  ("Priority (1=High):", "priority"),
                  ("Arrival Time:", "arrival")]
        self.entries = {}
        for label, key in fields:
            tk.Label(left, text=label, bg="#313244",
                    fg="#cdd6f4", font=("Helvetica", 10)).pack(anchor="w", padx=15)
            e = tk.Entry(left, bg="#45475a", fg="white",
                        insertbackground="white", font=("Helvetica", 11))
            e.pack(fill=tk.X, padx=15, pady=(0,8))
            self.entries[key] = e

        tk.Button(left, text="➕ Add Task", command=self.add_task,
                 bg="#a6e3a1", fg="#1e1e2e", font=("Helvetica", 11, "bold"),
                 relief="flat", cursor="hand2").pack(fill=tk.X, padx=15, pady=5)

        # Algorithm selector
        tk.Label(left, text="Scheduling Algorithm:",
                bg="#313244", fg="#cdd6f4",
                font=("Helvetica", 10)).pack(anchor="w", padx=15, pady=(10,0))
        self.algo_var = tk.StringVar(value="FCFS")
        algo_menu = ttk.Combobox(left, textvariable=self.algo_var,
                                values=["FCFS", "Round Robin", "Priority"],
                                state="readonly", font=("Helvetica", 11))
        algo_menu.pack(fill=tk.X, padx=15, pady=(0,10))

        tk.Button(left, text="▶ Run Simulation", command=self.run_simulation,
                 bg="#89b4fa", fg="#1e1e2e", font=("Helvetica", 11, "bold"),
                 relief="flat", cursor="hand2").pack(fill=tk.X, padx=15, pady=5)

        tk.Button(left, text="🔄 Reset", command=self.reset,
                 bg="#f38ba8", fg="#1e1e2e", font=("Helvetica", 11, "bold"),
                 relief="flat", cursor="hand2").pack(fill=tk.X, padx=15, pady=5)

        # Task list
        tk.Label(left, text="Task Queue:", bg="#313244",
                fg="#89dceb", font=("Helvetica", 11, "bold")).pack(anchor="w", padx=15, pady=(15,5))
        self.task_listbox = tk.Listbox(left, bg="#45475a", fg="#cdd6f4",
                                      font=("Courier", 9), height=10)
        self.task_listbox.pack(fill=tk.BOTH, expand=True, padx=15, pady=(0,15))

        # Right panel
        right = tk.Frame(main_frame, bg="#1e1e2e")
        right.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Stats bar
        self.stats_var = tk.StringVar(value="Total Energy: -- J  |  Avg Wait: -- ms  |  Throughput: --")
        stats_bar = tk.Label(right, textvariable=self.stats_var,
                            bg="#313244", fg="#a6e3a1",
                            font=("Helvetica", 10, "bold"), pady=6)
        stats_bar.pack(fill=tk.X, pady=(0,5))

        # Charts
        self.fig, self.axes = plt.subplots(3, 1, figsize=(8, 7))
        self.fig.patch.set_facecolor("#1e1e2e")
        for ax in self.axes:
            ax.set_facecolor("#313244")
            ax.tick_params(colors="#cdd6f4")
            for spine in ax.spines.values():
                spine.set_edgecolor("#45475a")

        self.canvas = FigureCanvasTkAgg(self.fig, master=right)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def add_task(self):
        try:
            burst = int(self.entries["burst"].get())
            priority = int(self.entries["priority"].get())
            arrival = int(self.entries["arrival"].get())
            task = Task(self.task_counter, burst, priority, arrival)
            self.tasks.append(task)
            self.task_listbox.insert(tk.END,
                f"T{self.task_counter} | Burst:{burst} | Pri:{priority} | Arr:{arrival}")
            self.task_counter += 1
            for e in self.entries.values():
                e.delete(0, tk.END)
        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid integer values!")

    def run_simulation(self):
        if not self.tasks:
            messagebox.showwarning("No Tasks", "Please add at least one task!")
            return
        algo = self.algo_var.get()
        tasks_copy = [Task(t.task_id, t.burst_time, t.priority, t.arrival_time)
                     for t in self.tasks]
        if algo == "FCFS":
            completed, log = fcfs(tasks_copy)
        elif algo == "Round Robin":
            completed, log = round_robin(tasks_copy)
        else:
            completed, log = priority_scheduling(tasks_copy)

        self.draw_charts(log, completed, algo)

        total_energy = sum(t.energy_consumed for t in completed)
        avg_wait = sum(t.waiting_time for t in completed) / len(completed)
        throughput = len(completed)
        self.stats_var.set(
            f"Total Energy: {total_energy:.2f} J  |  "
            f"Avg Wait: {avg_wait:.1f} ms  |  "
            f"Throughput: {throughput} tasks  |  Algorithm: {algo}")

    def draw_charts(self, log, completed, algo):
        colors = {"LOW": "#a6e3a1", "MID": "#f9e2af", "HIGH": "#f38ba8"}
        for ax in self.axes:
            ax.clear()
            ax.set_facecolor("#313244")
            ax.tick_params(colors="#cdd6f4")

        # Gantt Chart
        ax1 = self.axes[0]
        for i, entry in enumerate(log):
            color = colors.get(entry.get("dvfs", "MID"), "#89b4fa")
            ax1.broken_barh([(entry["start"], entry["end"] - entry["start"])],
                           (i * 12, 10), facecolors=color, edgecolor="#1e1e2e")
            ax1.text(entry["start"] + 0.2, i * 12 + 3,
                    f"T{entry['task_id']}", color="#1e1e2e",
                    fontsize=7, fontweight="bold")
        ax1.set_title(f"Gantt Chart — {algo}", color="#cba6f7", fontsize=10)
        ax1.set_xlabel("Time (ms)", color="#cdd6f4", fontsize=8)
        patches = [mpatches.Patch(color=c, label=l) for l, c in colors.items()]
        ax1.legend(handles=patches, loc="upper right",
                  fontsize=7, facecolor="#45475a", labelcolor="#cdd6f4")

        # Frequency chart
        ax2 = self.axes[1]
        task_ids = [f"T{e['task_id']}" for e in log]
        freqs = [e["freq"] for e in log]
        ax2.plot(task_ids, freqs, color="#89b4fa", marker="o",
                linewidth=2, markersize=5)
        ax2.set_title("CPU Frequency per Task", color="#cba6f7", fontsize=10)
        ax2.set_ylabel("Frequency", color="#cdd6f4", fontsize=8)
        ax2.set_ylim(0, 1.2)

        # Temperature chart
        ax3 = self.axes[2]
        temps = [e["temp"] for e in log]
        ax3.plot(task_ids, temps, color="#f38ba8", marker="s",
                linewidth=2, markersize=5)
        ax3.axhline(y=80, color="#fab387", linestyle="--",
                   linewidth=1, label="Thermal Limit")
        ax3.set_title("CPU Temperature Over Time", color="#cba6f7", fontsize=10)
        ax3.set_ylabel("Temp (°C)", color="#cdd6f4", fontsize=8)
        ax3.legend(fontsize=7, facecolor="#45475a", labelcolor="#cdd6f4")

        self.fig.tight_layout(pad=2.0)
        self.canvas.draw()

    def reset(self):
        self.tasks = []
        self.task_counter = 1
        self.task_listbox.delete(0, tk.END)
        self.stats_var.set("Total Energy: -- J  |  Avg Wait: -- ms  |  Throughput: --")
        for ax in self.axes:
            ax.clear()
            ax.set_facecolor("#313244")
        self.canvas.draw()

def launch():
    root = tk.Tk()
    app = CPUSchedulerGUI(root)
    root.mainloop()

if __name__ == "__main__":
    launch()
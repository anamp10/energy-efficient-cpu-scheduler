import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from scheduler_engine.scheduler import Task, fcfs, round_robin, priority_scheduling
import matplotlib.pyplot as plt
import pandas as pd
import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def generate_sample_tasks(n=8):
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
    for name, func in algos.items():
        copies = [Task(t.task_id, t.burst_time, t.priority, t.arrival_time)
                 for t in tasks]
        completed, log = func(copies)
        total_energy = sum(t.energy_consumed for t in completed)
        avg_wait = sum(t.waiting_time for t in completed) / len(completed)
        avg_turnaround = sum(t.turnaround_time for t in completed) / len(completed)
        results[name] = {
            "Total Energy (J)": round(total_energy, 2),
            "Avg Wait Time (ms)": round(avg_wait, 2),
            "Avg Turnaround (ms)": round(avg_turnaround, 2),
            "Tasks Completed": len(completed)
        }
    return results

class AnalyticsWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Analytics & Algorithm Comparison")
        self.root.geometry("1000x700")
        self.root.configure(bg="#1e1e2e")
        self.build_ui()

    def build_ui(self):
        tk.Label(self.root, text="📊 Algorithm Performance Comparison",
                font=("Helvetica", 16, "bold"),
                bg="#1e1e2e", fg="#cba6f7").pack(pady=10)

        btn_frame = tk.Frame(self.root, bg="#1e1e2e")
        btn_frame.pack(pady=5)

        tk.Button(btn_frame, text="▶ Run Comparison",
                 command=self.run_comparison,
                 bg="#a6e3a1", fg="#1e1e2e",
                 font=("Helvetica", 11, "bold"),
                 relief="flat", cursor="hand2").pack(side=tk.LEFT, padx=10)

        tk.Button(btn_frame, text="💾 Export CSV",
                 command=self.export_csv,
                 bg="#89b4fa", fg="#1e1e2e",
                 font=("Helvetica", 11, "bold"),
                 relief="flat", cursor="hand2").pack(side=tk.LEFT, padx=10)

        # Table frame
        table_frame = tk.Frame(self.root, bg="#313244")
        table_frame.pack(fill=tk.X, padx=20, pady=10)

        cols = ["Algorithm", "Total Energy (J)",
                "Avg Wait Time (ms)", "Avg Turnaround (ms)", "Tasks Completed"]
        self.tree = ttk.Treeview(table_frame, columns=cols,
                                show="headings", height=4)
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview",
                       background="#313244",
                       foreground="#cdd6f4",
                       rowheight=28,
                       fieldbackground="#313244",
                       font=("Helvetica", 10))
        style.configure("Treeview.Heading",
                       background="#45475a",
                       foreground="#cba6f7",
                       font=("Helvetica", 10, "bold"))
        for col in cols:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=180, anchor="center")
        self.tree.pack(fill=tk.X)

        # Chart frame
        chart_frame = tk.Frame(self.root, bg="#1e1e2e")
        chart_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        self.fig, self.axes = plt.subplots(1, 3, figsize=(10, 4))
        self.fig.patch.set_facecolor("#1e1e2e")
        for ax in self.axes:
            ax.set_facecolor("#313244")
            ax.tick_params(colors="#cdd6f4")
            for spine in ax.spines.values():
                spine.set_edgecolor("#45475a")

        self.canvas = FigureCanvasTkAgg(self.fig, master=chart_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        self.results = None

    def run_comparison(self):
        tasks = generate_sample_tasks(8)
        self.results = run_all_algorithms(tasks)

        # Clear table
        for row in self.tree.get_children():
            self.tree.delete(row)

        # Fill table
        for algo, metrics in self.results.items():
            self.tree.insert("", tk.END, values=[
                algo,
                metrics["Total Energy (J)"],
                metrics["Avg Wait Time (ms)"],
                metrics["Avg Turnaround (ms)"],
                metrics["Tasks Completed"]
            ])

        self.draw_charts()

    def draw_charts(self):
        if not self.results:
            return

        algos = list(self.results.keys())
        colors = ["#a6e3a1", "#89b4fa", "#f38ba8"]
        metrics = ["Total Energy (J)", "Avg Wait Time (ms)", "Avg Turnaround (ms)"]
        titles = ["Energy Consumption", "Avg Wait Time", "Avg Turnaround Time"]

        for i, (metric, title) in enumerate(zip(metrics, titles)):
            ax = self.axes[i]
            ax.clear()
            ax.set_facecolor("#313244")
            ax.tick_params(colors="#cdd6f4")
            values = [self.results[a][metric] for a in algos]
            bars = ax.bar(algos, values, color=colors, edgecolor="#1e1e2e")
            ax.set_title(title, color="#cba6f7", fontsize=9, fontweight="bold")
            ax.set_ylabel(metric, color="#cdd6f4", fontsize=8)
            for bar, val in zip(bars, values):
                ax.text(bar.get_x() + bar.get_width()/2,
                       bar.get_height() + 0.1,
                       str(val), ha="center",
                       color="#cdd6f4", fontsize=8)

        self.fig.tight_layout(pad=2.0)
        self.canvas.draw()

    def export_csv(self):
        if not self.results:
            import tkinter.messagebox as mb
            mb.showwarning("No Data", "Run comparison first!")
            return
        df = pd.DataFrame(self.results).T
        df.to_csv("analytics_results.csv")
        import tkinter.messagebox as mb
        mb.showinfo("Exported!", "Results saved to analytics_results.csv ✅")

def launch():
    root = tk.Tk()
    app = AnalyticsWindow(root)
    root.mainloop()

if __name__ == "__main__":
    launch()
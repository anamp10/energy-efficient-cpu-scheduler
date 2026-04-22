import tkinter as tk
from tkinter import ttk
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from gui_dashboard.gui import CPUSchedulerGUI
from analytics.comparator import AnalyticsWindow

class MainMenu:
    def __init__(self, root):
        self.root = root
        self.root.title("Energy-Efficient CPU Scheduler")
        self.root.geometry("500x400")
        self.root.configure(bg="#1e1e2e")
        self.build_ui()

    def build_ui(self):
        # Title
        tk.Label(self.root,
                text="⚡ Energy-Efficient CPU Scheduler",
                font=("Helvetica", 16, "bold"),
                bg="#1e1e2e", fg="#cba6f7").pack(pady=30)

        tk.Label(self.root,
                text="DVFS-Based Power-Aware Scheduling Simulation",
                font=("Helvetica", 10),
                bg="#1e1e2e", fg="#6c7086").pack(pady=(0,30))

        # Buttons
        tk.Button(self.root,
                 text="▶  Launch Scheduler Simulator",
                 command=self.open_scheduler,
                 bg="#a6e3a1", fg="#1e1e2e",
                 font=("Helvetica", 13, "bold"),
                 relief="flat", cursor="hand2",
                 width=30, pady=10).pack(pady=10)

        tk.Button(self.root,
                 text="📊  Open Analytics Dashboard",
                 command=self.open_analytics,
                 bg="#89b4fa", fg="#1e1e2e",
                 font=("Helvetica", 13, "bold"),
                 relief="flat", cursor="hand2",
                 width=30, pady=10).pack(pady=10)

        tk.Button(self.root,
                 text="❌  Exit",
                 command=self.root.destroy,
                 bg="#f38ba8", fg="#1e1e2e",
                 font=("Helvetica", 13, "bold"),
                 relief="flat", cursor="hand2",
                 width=30, pady=10).pack(pady=10)

        # Footer
        tk.Label(self.root,
                text="CSE-316 | CA2 Project",
                font=("Helvetica", 9),
                bg="#1e1e2e", fg="#6c7086").pack(side=tk.BOTTOM, pady=15)

    def open_scheduler(self):
        scheduler_win = tk.Toplevel(self.root)
        CPUSchedulerGUI(scheduler_win)

    def open_analytics(self):
        analytics_win = tk.Toplevel(self.root)
        AnalyticsWindow(analytics_win)

if __name__ == "__main__":
    root = tk.Tk()
    app = MainMenu(root)
    root.mainloop()
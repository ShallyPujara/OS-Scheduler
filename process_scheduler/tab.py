import tkinter as tk
from tkinter import ttk, messagebox
from .scheduler import (
    fcfs_scheduling, 
    round_robin_scheduling,
    sjf_scheduling,
    priority_scheduling,
    srtf_scheduling
)
from .visualization import plot_schedule

class ProcessSchedulerTab:
    def __init__(self, parent):
        self.frame = ttk.Frame(parent)
        self.frame.pack(expand=True, fill="both") 
        self.frame.pack_propagate(True)
        
        # ===== HEADER =====
        header = tk.Frame(self.frame, bg="#4a6fa5")
        tk.Label(header, text="PROCESS SCHEDULER", font=("Helvetica", 18, "bold"), 
                bg="#4a6fa5", fg="white").pack(pady=15)
        header.pack(fill="x", pady=(0, 20))

        # ===== INPUT FRAME =====
        input_frame = tk.LabelFrame(self.frame, text="Process Parameters",
                                  font=("Helvetica", 11, "bold"),
                                  padx=15, pady=15)
        input_frame.pack(fill="x", pady=10)
        
        # Input Grid
        input_grid = tk.Frame(input_frame)
        input_grid.pack(fill="x")
        
        # Process ID
        tk.Label(input_grid, text="Process ID:").grid(row=0, column=0, sticky="e", padx=5)
        self.pid_entry = ttk.Entry(input_grid, width=10)
        self.pid_entry.grid(row=0, column=1, sticky="w", pady=5)
        
        # Burst Time
        tk.Label(input_grid, text="Burst Time:").grid(row=0, column=2, sticky="e", padx=5)
        self.burst_entry = ttk.Entry(input_grid, width=10)
        self.burst_entry.grid(row=0, column=3, sticky="w", pady=5)
        
        # Arrival Time
        tk.Label(input_grid, text="Arrival Time:").grid(row=1, column=0, sticky="e", padx=5)
        self.arrival_entry = ttk.Entry(input_grid, width=10)
        self.arrival_entry.grid(row=1, column=1, sticky="w", pady=5)
        
        # Priority
        tk.Label(input_grid, text="Priority:").grid(row=1, column=2, sticky="e", padx=5)
        self.priority_entry = ttk.Entry(input_grid, width=10)
        self.priority_entry.grid(row=1, column=3, sticky="w", pady=5)
        
        # Action Buttons
        btn_frame = tk.Frame(input_frame)
        btn_frame.pack(pady=10)
        
        ttk.Button(btn_frame, text="Add Process", command=self.add_process).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Remove Selected", command=self.remove_process).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Clear All", command=self.clear_processes).pack(side="left", padx=5)

        # ===== PROCESS TABLE =====
        table_frame = tk.LabelFrame(self.frame, text="Process Queue",
                                  font=("Helvetica", 11, "bold"),
                                  padx=15, pady=15)
        table_frame.pack(fill="both", expand=True, pady=10)
        
        self.process_list = ttk.Treeview(table_frame, columns=("PID", "Burst", "Arrival", "Priority"), 
                                       show="headings", height=8)
        
        # Configure columns
        for col in ["PID", "Burst", "Arrival", "Priority"]:
            self.process_list.heading(col, text=col)
            self.process_list.column(col, width=100, anchor="center")
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.process_list.yview)
        self.process_list.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        self.process_list.pack(fill="both", expand=True)

        # ===== ALGORITHM SELECTION =====
        algo_frame = tk.LabelFrame(self.frame, text="Scheduling Algorithm",
                                 font=("Helvetica", 11, "bold"),
                                 padx=15, pady=15)
        algo_frame.pack(fill="x", pady=10)
        
        self.algorithm_var = tk.StringVar(value="FCFS")
        
        algorithms = [
            ("FCFS", "First-Come First-Served"),
            ("SJF", "Shortest Job First"),
            ("Priority", "Priority Scheduling"),
            ("Round Robin", "Round Robin"),
            ("SRTF", "Shortest Remaining Time First")
        ]
        
        for i, (value, text) in enumerate(algorithms):
            ttk.Radiobutton(algo_frame, text=text, variable=self.algorithm_var, 
                          value=value).grid(row=i//2, column=i%2, sticky="w", padx=5, pady=2)
        
        quantum_frame = tk.Frame(algo_frame)
        quantum_frame.grid(row=2, column=1, sticky="w")
        
        tk.Label(quantum_frame, text="Time Quantum:").pack(side="left")
        self.quantum_entry = ttk.Entry(quantum_frame, width=5)
        self.quantum_entry.pack(side="left", padx=5)
        self.quantum_entry.insert(0, "2")

        run_frame = tk.Frame(self.frame)
        run_frame.pack(pady=15)

        style = ttk.Style()
        style.configure('Accent.TButton', foreground='white', background='#4a6fa5')
        
        self.run_btn = ttk.Button(run_frame, 
                  text="▶ Run Scheduling", 
                  command=self.run_scheduler,
                  style='Accent.TButton')
        self.run_btn.pack(side="left", padx=5)
        self.frame.update()
        
        ttk.Button(run_frame,
                  text="Clear Metrics",
                  command=self.clear_metrics).pack(side="left", padx=5)

        # ===== STATUS BAR =====
        self.status_var = tk.StringVar(value="Ready to schedule processes")
        ttk.Label(self.frame, textvariable=self.status_var, relief="sunken",
                anchor="w").pack(fill="x")

    def add_process(self):
        try:
            pid = int(self.pid_entry.get())
            burst = int(self.burst_entry.get())
            arrival = int(self.arrival_entry.get())
            priority = int(self.priority_entry.get() or 0)
            
            self.process_list.insert("", "end", values=(pid, burst, arrival, priority))
            
            # Clear entries
            self.pid_entry.delete(0, tk.END)
            self.burst_entry.delete(0, tk.END)
            self.arrival_entry.delete(0, tk.END)
            self.priority_entry.delete(0, tk.END)
            
            self.status_var.set(f"Process P{pid} added")
            
        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid numbers!")

    def remove_process(self):
        selected = self.process_list.selection()
        if selected:
            pid = self.process_list.item(selected[0], "values")[0]
            self.process_list.delete(selected[0])
            self.status_var.set(f"Process P{pid} removed")
        else:
            messagebox.showwarning("Selection Error", "No process selected")

    def clear_processes(self):
        for item in self.process_list.get_children():
            self.process_list.delete(item)
        self.status_var.set("All processes cleared")

    def clear_metrics(self):
        """Remove waiting/turnaround time columns"""
        self.process_list["columns"] = ("PID", "Burst", "Arrival", "Priority")
        for col in self.process_list["columns"]:
            self.process_list.heading(col, text=col)
        self.status_var.set("Metrics cleared")

    def run_scheduler(self):
        processes = []
        for item in self.process_list.get_children():
            pid, burst, arrival, priority = self.process_list.item(item, "values")
            processes.append({
                "process_id": int(pid),
                "burst_time": int(burst),
                "arrival_time": int(arrival),
                "priority": int(priority)
            })
        
        if not processes:
            messagebox.showerror("Error", "No processes to schedule!")
            return
        
        algorithm = self.algorithm_var.get()
        quantum = int(self.quantum_entry.get()) if algorithm == "Round Robin" else None
        
        try:
            self.status_var.set(f"Running {algorithm}...")
            self.frame.update()
            
            if algorithm == "FCFS":
                result = fcfs_scheduling(processes)
            elif algorithm == "SJF":
                result = sjf_scheduling(processes)
            elif algorithm == "Priority":
                result = priority_scheduling(processes)
            elif algorithm == "Round Robin":
                result = round_robin_scheduling(processes, quantum)
            elif algorithm == "SRTF":
                result = srtf_scheduling(processes)
            
            # Update table with metrics
            self.process_list["columns"] = ("PID", "Burst", "Arrival", "Priority", "Waiting", "Turnaround")
            for col in self.process_list["columns"]:
                self.process_list.heading(col, text=col)
                self.process_list.column(col, width=80, anchor="center")
            
            for item in self.process_list.get_children():
                values = list(self.process_list.item(item, "values"))
                pid = int(values[0])
                new_values = values + [
                    result["waiting_times"][pid],
                    result["turnaround_times"][pid]
                ]
                self.process_list.item(item, values=new_values)
            
            # Show visualization
            plot_schedule(result)
            
            avg_wait = sum(result["waiting_times"].values()) / len(processes)
            avg_turn = sum(result["turnaround_times"].values()) / len(processes)
            self.status_var.set(
                f"{algorithm} completed | Avg Wait: {avg_wait:.1f} | Avg Turnaround: {avg_turn:.1f}"
            )
            
        except Exception as e:
            messagebox.showerror("Error", f"Scheduling failed: {str(e)}")
            self.status_var.set("Error during scheduling")
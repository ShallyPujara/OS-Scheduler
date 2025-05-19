import tkinter as tk
from tkinter import ttk, messagebox
from .algorithms import look_algorithm, c_look_algorithm
from .visualization import plot_disk_movement

class DiskSchedulerTab:
    def __init__(self, parent):
        self.frame = ttk.Frame(parent)
        self.frame.config(padding=20)
        
        # Header
        header = tk.Frame(self.frame, bg="#4a6fa5")
        tk.Label(header, text="DISK SCHEDULER", font=("Helvetica", 18, "bold"), 
                bg="#4a6fa5", fg="white").pack(pady=15)
        header.pack(fill="x", pady=(0, 20))
        
        # Input Frame
        input_frame = tk.LabelFrame(self.frame, text="Disk Request Parameters",
                                  font=("Helvetica", 11, "bold"),
                                  padx=15, pady=15)
        input_frame.pack(fill="x", pady=10)
        
        # Request Entry
        tk.Label(input_frame, text="Track Requests (comma separated):").grid(row=0, column=0, sticky="e", padx=5)
        self.requests_entry = ttk.Entry(input_frame, width=40)
        self.requests_entry.grid(row=0, column=1, pady=5)
        self.requests_entry.insert(0, "98, 183, 37, 122, 14, 124, 65, 67")
        
        # Head Position
        tk.Label(input_frame, text="Initial Head Position:").grid(row=1, column=0, sticky="e", padx=5)
        self.head_entry = ttk.Entry(input_frame, width=10)
        self.head_entry.grid(row=1, column=1, sticky="w", pady=5)
        self.head_entry.insert(0, "53")
        
        # Algorithm Selection
        tk.Label(input_frame, text="Algorithm:").grid(row=2, column=0, sticky="e", padx=5)
        self.algorithm_var = tk.StringVar(value="LOOK")
        ttk.Radiobutton(input_frame, text="LOOK", variable=self.algorithm_var, value="LOOK").grid(row=2, column=1, sticky="w")
        ttk.Radiobutton(input_frame, text="C-LOOK", variable=self.algorithm_var, value="C-LOOK").grid(row=3, column=1, sticky="w")
        
        # Direction (for LOOK)
        tk.Label(input_frame, text="Initial Direction:").grid(row=4, column=0, sticky="e", padx=5)
        self.direction_var = tk.StringVar(value="right")
        ttk.Combobox(input_frame, textvariable=self.direction_var, 
                    values=["right", "left"], width=7).grid(row=4, column=1, sticky="w")
        
        # Run Button
        ttk.Button(self.frame, text="Run Disk Scheduling", command=self.run_scheduler).pack(pady=20)
        
        # Results Frame
        results_frame = tk.LabelFrame(self.frame, text="Results",
                                    font=("Helvetica", 11, "bold"),
                                    padx=15, pady=15)
        results_frame.pack(fill="both", expand=True)
        
        self.results_text = tk.Text(results_frame, height=10, wrap="word")
        scrollbar = ttk.Scrollbar(results_frame, command=self.results_text.yview)
        self.results_text.config(yscrollcommand=scrollbar.set)
        
        scrollbar.pack(side="right", fill="y")
        self.results_text.pack(fill="both", expand=True)
    
    def run_scheduler(self):
        try:
            requests = [int(r.strip()) for r in self.requests_entry.get().split(",")]
            head = int(self.head_entry.get())
            
            if self.algorithm_var.get() == "LOOK":
                result = look_algorithm(requests, head, self.direction_var.get())
            else:
                result = c_look_algorithm(requests, head, self.direction_var.get())
            
            # Update results
            self.results_text.delete(1.0, tk.END)
            self.results_text.insert(tk.END, f"Algorithm: {self.algorithm_var.get()}\n")
            self.results_text.insert(tk.END, f"Initial Head Position: {head}\n")
            if 'direction' in result:
                self.results_text.insert(tk.END, f"Direction: {result['direction'].capitalize()}\n")
            self.results_text.insert(tk.END, f"\nService Sequence:\n{result['sequence']}\n")
            self.results_text.insert(tk.END, f"\nTotal Head Movement: {result['total_movement']} tracks")
            
            # Show visualization
            plot_disk_movement(head, result)
            
        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid numbers!")
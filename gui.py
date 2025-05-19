import tkinter as tk
from tkinter import ttk
from process_scheduler import ProcessSchedulerTab
from disk_scheduler import DiskSchedulerTab

class MainApplication:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Scheduler")
        self.root.geometry("1200x800")
        self.root.config(bg="#f0f2f5")

        style = ttk.Style()
        style.theme_use('clam')
        style.configure("TNotebook", background="#e2e8f0")
        style.configure("TNotebook.Tab", padding=[20, 5], font=('Helvetica', 10, 'bold'))

        self.notebook = ttk.Notebook(root)
        
        self.process_tab = ProcessSchedulerTab(self.notebook)
        self.disk_tab = DiskSchedulerTab(self.notebook)
        
        self.notebook.add(self.process_tab.frame, text="🖥️ Process Scheduling")
        self.notebook.add(self.disk_tab.frame, text="💾 Disk Scheduling")
        self.notebook.pack(expand=1, fill="both", padx=10, pady=10)

if __name__ == "__main__":
    root = tk.Tk()
    app = MainApplication(root)
    root.mainloop()
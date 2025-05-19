import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import numpy as np

def plot_schedule(schedule_data):
    schedule = schedule_data["schedule"]
    if not schedule:
        print("No schedule to visualize!")
        return

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8), 
                         gridspec_kw={'height_ratios': [3, 1]})
    
    unique_pids = list({p["process_id"] for p in schedule})
    colors = plt.cm.tab20(np.linspace(0, 1, len(unique_pids)))
    color_map = {pid: colors[i] for i, pid in enumerate(unique_pids)}

    for process in schedule:
        duration = process["end_time"] - process["start_time"]
        ax1.broken_barh([(process["start_time"], duration)],
                       (process["process_id"] - 0.4, 0.8),
                       facecolors=color_map[process["process_id"]],
                       edgecolor='black',
                       linewidth=0.5)

    ax1.set_title("Process Scheduling Gantt Chart", pad=15)
    ax1.set_xlabel("Time Units")
    ax1.set_ylabel("Process ID")
    ax1.set_yticks(unique_pids)
    ax1.set_yticklabels([f'P{pid}' for pid in unique_pids])
    ax1.grid(True, axis='x', linestyle='--')

    metrics = ['Waiting Time', 'Turnaround Time']
    for i, metric in enumerate(metrics):
        values = [schedule_data[f"{metric.lower().replace(' ', '_')}s"].get(pid, 0) 
                 for pid in unique_pids]
        ax2.bar(np.array(unique_pids) + (i*0.4) - 0.2, values, 0.4, 
               label=metric, color=[color_map[pid] for pid in unique_pids])

    ax2.set_title("Process Metrics")
    ax2.set_xticks(unique_pids)
    ax2.set_xticklabels([f'P{pid}' for pid in unique_pids])
    ax2.legend()
    ax2.grid(True, axis='y', linestyle='--')

    plt.tight_layout()
    plt.show()
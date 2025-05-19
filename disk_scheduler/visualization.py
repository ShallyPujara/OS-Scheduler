import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
import numpy as np

def plot_disk_movement(initial_head, result):
    sequence = [initial_head] + result["sequence"]
    x = range(len(sequence))
    y = sequence
    
    fig, ax = plt.subplots(figsize=(12, 6))
    
    points = np.array([x, y]).T.reshape(-1, 1, 2)
    segments = np.concatenate([points[:-1], points[1:]], axis=1)
    
    norm = plt.Normalize(min(y), max(y))
    lc = LineCollection(segments, cmap='viridis', norm=norm)
    lc.set_array(np.array(y))
    line = ax.add_collection(lc)
    
    ax.scatter(x, y, c='red', zorder=2)
    for i, (xi, yi) in enumerate(zip(x, y)):
        if i == 0:
            ax.annotate(f'Start: {yi}', (xi, yi), textcoords="offset points", xytext=(0,10), ha='center')
        else:
            ax.annotate(str(yi), (xi, yi), textcoords="offset points", xytext=(0,5), ha='center')
    
    ax.set_xlim(-0.5, len(sequence)-0.5)
    ax.set_ylim(min(y)-10, max(y)+10)
    ax.set_title(f"Disk Head Movement ({'LOOK' if 'direction' in result else 'C-LOOK'})")
    ax.set_xlabel("Step")
    ax.set_ylabel("Track Number")
    ax.grid(True)
    
    cbar = fig.colorbar(line, ax=ax)
    cbar.set_label('Track Position')
    
    plt.tight_layout()
    plt.show()
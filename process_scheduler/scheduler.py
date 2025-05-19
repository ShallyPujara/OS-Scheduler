ALGORITHM_COMPLEXITY = {
    "FCFS": {
        "time": {
            "best": "O(n) [already sorted]",
            "average": "O(n log n)",
            "worst": "O(n log n)"
        },
        "space": "O(n)",
        "description": "Simple but can lead to convoy effect"
    },
    "Round Robin": {
        "time": {
            "best": "O(n) [large quantum]",
            "average": "O(n log n)",
            "worst": "O(n²) [small quantum]"
        },
        "space": "O(n)",
        "description": "Fair but high context switching overhead"
    },
    "SJF": {
        "time": {
            "best": "O(n log n)",
            "average": "O(n²)",
            "worst": "O(n²)"
        },
        "space": "O(n)",
        "description": "Optimal for minimizing waiting time"
    },
    "Priority": {
        "time": {
            "best": "O(n log n)",
            "average": "O(n log n)",
            "worst": "O(n log n)"
        },
        "space": "O(n)",
        "description": "Can lead to starvation of low-priority processes"
    },
    "SRTF": {
        "time": {
            "best": "O(n log n)",
            "average": "O(n²)",
            "worst": "O(n²)"
        },
        "space": "O(n)",
        "description": "Preemptive SJF - optimal but complex"
    }
}

def calculate_waiting_time(schedule, processes):
    waiting_times = {}
    original_processes = {p["process_id"]: p for p in processes}
    
    for pid, process in original_processes.items():
        waiting_time = 0
        last_time = process["arrival_time"]
        
        executions = sorted([e for e in schedule if e["process_id"] == pid], 
                          key=lambda x: x["start_time"])
        
        for exec in executions:
            if exec["start_time"] > last_time:
                waiting_time += exec["start_time"] - last_time
            last_time = max(last_time, exec["end_time"])
        
        waiting_times[pid] = waiting_time
    
    return waiting_times

def calculate_turnaround_time(schedule, processes):
    turnaround_times = {}
    original_processes = {p["process_id"]: p for p in processes}
    
    for pid, process in original_processes.items():
        executions = [e for e in schedule if e["process_id"] == pid]
        if not executions:
            continue
        last_execution = max(executions, key=lambda x: x["end_time"])
        turnaround_times[pid] = last_execution["end_time"] - process["arrival_time"]
    
    return turnaround_times

def fcfs_scheduling(processes):
    processes_sorted = sorted(processes, key=lambda x: x['arrival_time'])
    time = 0
    schedule = []

    for process in processes_sorted:
        start_time = max(time, process["arrival_time"])
        end_time = start_time + process["burst_time"]
        schedule.append({
            "process_id": process["process_id"],
            "start_time": start_time,
            "end_time": end_time
        })
        time = end_time

    return {
        "schedule": schedule,
        "waiting_times": calculate_waiting_time(schedule, processes),
        "turnaround_times": calculate_turnaround_time(schedule, processes),
        "complexity": ALGORITHM_COMPLEXITY["FCFS"]
    }

    
def round_robin_scheduling(processes, time_quantum=2):
    if not processes:
        return {"schedule": [], "waiting_times": {}, "turnaround_times": {}, "complexity": ALGORITHM_COMPLEXITY["Round Robin"]}
    
    remaining_processes = [p.copy() for p in processes]
    remaining_processes.sort(key=lambda x: x['arrival_time'])
    
    time = 0
    schedule = []
    queue = []
    
    while remaining_processes or queue:
        while remaining_processes and remaining_processes[0]['arrival_time'] <= time:
            queue.append(remaining_processes.pop(0))
        
        if not queue:
            time = remaining_processes[0]['arrival_time']
            continue
            
        process = queue.pop(0)
        start_time = time
        executed_time = min(time_quantum, process["burst_time"])
        end_time = start_time + executed_time
        
        schedule.append({
            "process_id": process["process_id"],
            "start_time": start_time,
            "end_time": end_time
        })
        
        process["burst_time"] -= executed_time
        time = end_time
        
        while remaining_processes and remaining_processes[0]['arrival_time'] <= time:
            queue.append(remaining_processes.pop(0))
        
        if process["burst_time"] > 0:
            queue.append(process)
    
    return {
        "schedule": schedule,
        "waiting_times": calculate_waiting_time(schedule, processes),
        "turnaround_times": calculate_turnaround_time(schedule, processes),
        "complexity": ALGORITHM_COMPLEXITY["Round Robin"]
    }


def sjf_scheduling(processes, preemptive=False):
    if not processes:
        return {"schedule": [], "waiting_times": {}, "turnaround_times": {}}
    
    if preemptive:
        return srtf_scheduling(processes)
    
    processes_sorted = sorted(processes, key=lambda x: (x['burst_time'], x['arrival_time']))
    time = 0
    schedule = []
    
    for process in processes_sorted:
        start_time = max(time, process["arrival_time"])
        end_time = start_time + process["burst_time"]
        schedule.append({
            "process_id": process["process_id"],
            "start_time": start_time,
            "end_time": end_time
        })
        time = end_time
    
    return {
        "schedule": schedule,
        "waiting_times": calculate_waiting_time(schedule, processes),
        "turnaround_times": calculate_turnaround_time(schedule, processes),
        "complexity": ALGORITHM_COMPLEXITY["SJF"]

    }

def priority_scheduling(processes):
    processes_sorted = sorted(processes, key=lambda x: (x['priority'], x['arrival_time']))
    time = 0
    schedule = []
    
    for process in processes_sorted:
        start_time = max(time, process["arrival_time"])
        end_time = start_time + process["burst_time"]
        schedule.append({
            "process_id": process["process_id"],
            "start_time": start_time,
            "end_time": end_time
        })
        time = end_time
    
    return {
        "schedule": schedule,
        "waiting_times": calculate_waiting_time(schedule, processes),
        "turnaround_times": calculate_turnaround_time(schedule, processes),
        "complexity": ALGORITHM_COMPLEXITY["Priority"]
    }

def srtf_scheduling(processes):
    """Shortest Remaining Time First (preemptive SJF)"""
    if not processes:
        return {"schedule": [], "waiting_times": {}, "turnaround_times": {}}
    
    remaining_processes = [p.copy() for p in processes]
    remaining_processes.sort(key=lambda x: x['arrival_time'])
    
    time = 0
    schedule = []
    current_process = None
    queue = []
    
    while remaining_processes or queue or current_process:
        while remaining_processes and remaining_processes[0]['arrival_time'] <= time:
            new_process = remaining_processes.pop(0)
            queue.append(new_process)
            if current_process and new_process['burst_time'] < current_process['burst_time']:
                if schedule and schedule[-1]["process_id"] == current_process["process_id"]:
                    schedule[-1]["end_time"] = time
                queue.append(current_process)
                current_process = None
        
        if not current_process and queue:
            queue.sort(key=lambda x: x['burst_time'])
            current_process = queue.pop(0)
            schedule.append({
                "process_id": current_process["process_id"],
                "start_time": time,
                "end_time": time
            })
        
        if current_process:
            current_process['burst_time'] -= 1
            time += 1
            schedule[-1]["end_time"] = time
            
            if current_process['burst_time'] == 0:
                current_process = None
        
        elif remaining_processes:
            time = remaining_processes[0]['arrival_time']
    
    # Merge adjacent intervals for same process
    merged_schedule = []
    for event in schedule:
        if merged_schedule and merged_schedule[-1]["process_id"] == event["process_id"] and \
           merged_schedule[-1]["end_time"] == event["start_time"]:
            merged_schedule[-1]["end_time"] = event["end_time"]
        else:
            merged_schedule.append(event)
    
    return {
        "schedule": merged_schedule,
        "waiting_times": calculate_waiting_time(merged_schedule, processes),
        "turnaround_times": calculate_turnaround_time(merged_schedule, processes),
        "complexity": ALGORITHM_COMPLEXITY["SRTF"]
    }
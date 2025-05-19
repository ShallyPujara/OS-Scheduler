def look_algorithm(requests, head, direction="right"):
    sequence = []
    left = [r for r in requests if r < head]
    right = [r for r in requests if r >= head]
    
    left.sort(reverse=True)
    right.sort()
    
    if direction == "right":
        sequence.extend(right)
        sequence.extend(left)
    else:
        sequence.extend(left)
        sequence.extend(right)
    
    total_movement = abs(head - sequence[0])
    for i in range(1, len(sequence)):
        total_movement += abs(sequence[i] - sequence[i-1])
    
    return {
        "sequence": sequence,
        "total_movement": total_movement,
        "direction": direction
    }

def c_look_algorithm(requests, head, direction="right"):
    sequence = []
    left = [r for r in requests if r < head]
    right = [r for r in requests if r >= head]
    
    left.sort()
    right.sort()
    
    if direction == "right":
        sequence.extend(right)
        sequence.extend(left)
    else:
        sequence.extend(left[::-1])
        sequence.extend(right[::-1])
    
    total_movement = abs(head - sequence[0])
    for i in range(1, len(sequence)):
        total_movement += abs(sequence[i] - sequence[i-1])
    
    return {
        "sequence": sequence,
        "total_movement": total_movement,
        "direction": direction
    }
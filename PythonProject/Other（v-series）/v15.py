def nsm (heaps):
    nsm = 0
    for heap in heaps:
        nsm ^= heap
    if nsm == 0:
        print("Current player is in a losing position (with optimal play).")
        return None
    for i in range(len(heaps)):
        target = heaps[i] ^ nsm
        if target < heaps[i]:
            move = heaps[i] - target
            print(f"Take {move} from heap {i} (from {heaps[i]} to {target}).")
            return i, move
    return None
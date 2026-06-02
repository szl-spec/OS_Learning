def fcfs(requests, head):
    """先来先服务"""
    total_seek = 0
    current = head
    sequence = []
    for req in requests:
        sequence.append(req)
        total_seek += abs(req - current)
        current = req
    return total_seek, sequence

def sstf(requests, head):
    """最短寻道时间优先"""
    total_seek = 0
    current = head
    sequence = []
    pending = requests.copy()
    while pending:
        # 寻找距离最近的请求
        nearest = min(pending, key=lambda x: abs(x - current))
        sequence.append(nearest)
        total_seek += abs(nearest - current)
        current = nearest
        pending.remove(nearest)
    return total_seek, sequence

def scan(requests, head, direction="up", disk_size=200):
    """扫描算法 (电梯算法)"""
    total_seek = 0
    current = head
    sequence = []
    # 请求排序，并分为左右
    requests.sort()
    left = [r for r in requests if r < head]
    right = [r for r in requests if r >= head]
    
    if direction == "up":
        # 先向大号移动
        for r in right:
            sequence.append(r)
            total_seek += abs(r - current)
            current = r
        # 到达右端，如果左边还有请求，先移动到末端再折返
        if left:
            total_seek += (disk_size - 1 - current)
            current = disk_size - 1
            left.reverse() # 从大到小
            for r in left:
                sequence.append(r)
                total_seek += abs(current - r)
                current = r
    else: # down
        left.reverse()
        for r in left:
            sequence.append(r)
            total_seek += abs(current - r)
            current = r
        if right:
            total_seek += current # 移动到0
            current = 0
            right.sort()
            for r in right:
                sequence.append(r)
                total_seek += abs(r - current)
                current = r
    return total_seek, sequence

def c_scan(requests, head, direction="up", disk_size=200):
    """循环扫描算法"""
    total_seek = 0
    current = head
    sequence = []
    requests.sort()
    left = [r for r in requests if r < head]
    right = [r for r in requests if r >= head]
    
    if direction == "up":
        for r in right:
            sequence.append(r)
            total_seek += abs(r - current)
            current = r
        if left:
            total_seek += (disk_size - 1 - current) # 到末端
            total_seek += (disk_size - 1) # 末端回到0
            current = 0
            for r in left:
                sequence.append(r)
                total_seek += abs(r - current)
                current = r
    else: # down
        left.reverse()
        for r in left:
            sequence.append(r)
            total_seek += abs(current - r)
            current = r
        if right:
            total_seek += current # 到0
            total_seek += (disk_size - 1) # 从0直接到末端
            current = disk_size - 1
            right.reverse()
            for r in right:
                sequence.append(r)
                total_seek += abs(current - r)
                current = r
    return total_seek, sequence

# 主程序
if __name__ == "__main__":
    requests = [98, 183, 37, 122, 14, 124, 65, 67]
    head = 53
    disk_size = 200
    
    print(f"磁盘请求序列: {requests}")
    print(f"当前磁头位置: {head}")
    
    total, seq = fcfs(requests, head)
    print(f"\nFCFS 总寻道长度: {total}, 顺序: {seq}")
    
    total, seq = sstf(requests, head)
    print(f"SSTF 总寻道长度: {total}, 顺序: {seq}")
    
    total, seq = scan(requests, head, direction="up", disk_size=disk_size)
    print(f"SCAN (向上) 总寻道长度: {total}, 顺序: {seq}")
    
    total, seq = c_scan(requests, head, direction="up", disk_size=disk_size)
    print(f"C-SCAN (向上) 总寻道长度: {total}, 顺序: {seq}")

import random

# 进程控制块 PCB
class PCB:
    def __init__(self, pid, arrive, burst):
        self.pid = pid
        self.arrive = arrive
        self.burst = burst
        self.start = 0
        self.finish = 0
        self.turnaround = 0
        self.weighted_turnaround = 0


# FCFS 先来先服务
def fcfs(processes):

    processes.sort(key=lambda x: x.arrive)

    current_time = 0

    for p in processes:

        if current_time < p.arrive:
            current_time = p.arrive

        p.start = current_time
        p.finish = current_time + p.burst

        p.turnaround = p.finish - p.arrive
        p.weighted_turnaround = p.turnaround / p.burst

        current_time = p.finish

    return processes


# SJF 短作业优先（非抢占）
def sjf(processes):

    remaining = processes[:]
    finished = []
    current_time = 0

    while remaining:

        available = [p for p in remaining if p.arrive <= current_time]

        if not available:
            current_time = min(p.arrive for p in remaining)
            available = [p for p in remaining if p.arrive <= current_time]

        next_proc = min(available, key=lambda x: x.burst)

        remaining.remove(next_proc)

        next_proc.start = current_time
        next_proc.finish = current_time + next_proc.burst

        next_proc.turnaround = next_proc.finish - next_proc.arrive
        next_proc.weighted_turnaround = next_proc.turnaround / next_proc.burst

        current_time = next_proc.finish

        finished.append(next_proc)

    return finished


# 打印结果
def print_result(processes, name):

    print("\n=== {} 调度结果 ===".format(name))
    print("PID\t到达\t服务\t开始\t完成\t周转\t带权周转")

    total_turn = 0
    total_weight = 0

    for p in processes:

        print("{}\t{}\t{}\t{}\t{}\t{}\t{:.2f}".format(
            p.pid, p.arrive, p.burst,
            p.start, p.finish,
            p.turnaround, p.weighted_turnaround
        ))

        total_turn += p.turnaround
        total_weight += p.weighted_turnaround

    n = len(processes)

    print("平均周转时间:", total_turn / n)
    print("平均带权周转时间:", total_weight / n)


# 主程序
if __name__ == "__main__":

    processes = []

    print("随机生成5个进程")

    for i in range(5):
        arrive = random.randint(0,5)
        burst = random.randint(1,8)

        processes.append(PCB(i+1, arrive, burst))

        print("P{} 到达:{} 服务:{}".format(i+1, arrive, burst))

    # FCFS
    fcfs_result = fcfs(processes.copy())
    print_result(fcfs_result, "FCFS")

    # SJF
    new_proc = [PCB(p.pid, p.arrive, p.burst) for p in processes]
    sjf_result = sjf(new_proc)

    print_result(sjf_result, "SJF")
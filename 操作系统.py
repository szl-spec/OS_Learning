"""
实验一：进程调度模拟 (FCFS 和 SJF 非抢占式)
功能：随机生成进程，计算周转时间等指标。
"""

import random


class PCB:
    """进程控制块"""

    def __init__(self, pid, arrive_time, burst_time):
        self.pid = pid  # 进程ID
        self.arrive_time = arrive_time  # 到达时间
        self.burst_time = burst_time  # 服务时间
        self.start_time = 0  # 开始运行时间
        self.finish_time = 0  # 完成时间
        self.turnaround_time = 0  # 周转时间
        self.weighted_turnaround = 0  # 带权周转时间


def fcfs_schedule(processes):
    """先来先服务算法"""
    # 按照到达时间排序
    sorted_proc = sorted(processes, key=lambda x: x.arrive_time)
    current_time = 0
    for p in sorted_proc:
        if current_time < p.arrive_time:
            current_time = p.arrive_time
        p.start_time = current_time
        p.finish_time = current_time + p.burst_time
        p.turnaround_time = p.finish_time - p.arrive_time
        p.weighted_turnaround = p.turnaround_time / p.burst_time
        current_time = p.finish_time
    return sorted_proc


def sjf_schedule(processes):
    """短作业优先 (非抢占式)"""
    # 复制一份，避免修改原列表
    remaining = processes.copy()
    current_time = 0
    finished = []
    while remaining:
        # 筛选出到达时间 <= current_time 的进程
        available = [p for p in remaining if p.arrive_time <= current_time]
        if not available:
            # 若当前无进程，跳到下一个进程到达时间
            current_time = min(p.arrive_time for p in remaining)
            available = [p for p in remaining if p.arrive_time <= current_time]

        # 选择服务时间最短的
        next_proc = min(available, key=lambda x: x.burst_time)
        remaining.remove(next_proc)

        next_proc.start_time = current_time
        next_proc.finish_time = current_time + next_proc.burst_time
        next_proc.turnaround_time = next_proc.finish_time - next_proc.arrive_time
        next_proc.weighted_turnaround = next_proc.turnaround_time / next_proc.burst_time

        current_time = next_proc.finish_time
        finished.append(next_proc)
    return finished


def print_result(processes, algorithm_name):
    """打印调度结果"""
    print(f"\n=== {algorithm_name} 调度结果 ===")
    print("ID\t到达\t服务\t开始\t完成\t周转\t带权周转")
    total_turn = 0
    total_weight = 0
    for p in processes:
        print(f"{p.pid}\t{p.arrive_time}\t{p.burst_time}\t{p.start_time}\t"
              f"{p.finish_time}\t{p.turnaround_time}\t{p.weighted_turnaround:.2f}")
        total_turn += p.turnaround_time
        total_weight += p.weighted_turnaround

    avg_turn = total_turn / len(processes)
    avg_weight = total_weight / len(processes)
    print(f"平均周转时间: {avg_turn:.2f}")
    print(f"平均带权周转时间: {avg_weight:.2f}")


# 测试
if __name__ == "__main__":
    # 随机生成 5 个进程
    processes = []
    for i in range(5):
        arrive = random.randint(0, 5)
        burst = random.randint(1, 8)
        processes.append(PCB(i + 1, arrive, burst))

    print("随机生成的进程：")
    for p in processes:
        print(f"进程ID:{p.pid}, 到达时间:{p.arrive_time}, 服务时间:{p.burst_time}")

    # FCFS
    fcfs_result = fcfs_schedule(processes)
    print_result(fcfs_result, "FCFS")

    # SJF (需要重新创建对象，因为FCFS修改了进程对象的属性)
    new_procs = [PCB(p.pid, p.arrive_time, p.burst_time) for p in processes]
    sjf_result = sjf_schedule(new_procs)
    print_result(sjf_result, "SJF")
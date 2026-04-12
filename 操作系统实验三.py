import numpy as np

class Banker:
    def __init__(self, available, max_matrix, allocation):
        """
        available: 可用资源向量 (list)
        max_matrix: 最大需求矩阵 (2D list)
        allocation: 已分配矩阵 (2D list)
        """
        self.available = np.array(available)
        self.max = np.array(max_matrix)
        self.allocation = np.array(allocation)
        self.need = self.max - self.allocation
        self.n_processes = self.max.shape[0]
        self.n_resources = self.max.shape[1]

    def is_safe(self):
        """安全性检查，返回 (是否安全, 安全序列)"""
        work = self.available.copy()
        finish = [False] * self.n_processes
        safe_sequence = []

        while len(safe_sequence) < self.n_processes:
            allocated = False
            for i in range(self.n_processes):
                if not finish[i] and np.all(self.need[i] <= work):
                    # 可以分配
                    work += self.allocation[i]
                    finish[i] = True
                    safe_sequence.append(i)
                    allocated = True
                    break
            
            if not allocated:
                # 没有进程可以分配，系统不安全
                return False, []

        return True, safe_sequence

    def request_resources(self, pid, request):
        """进程 pid 请求 request 资源"""
        request = np.array(request)
        if np.any(request > self.need[pid]):
            print(f"进程 {pid} 请求超过所需，错误！")
            return False
        
        if np.any(request > self.available):
            print(f"进程 {pid} 请求超过可用资源，需等待。")
            return False

        # 试探分配
        self.available -= request
        self.allocation[pid] += request
        self.need[pid] -= request

        # 检查安全性
        safe, seq = self.is_safe()
        if safe:
            print(f"分配成功！安全序列为：{seq}")
            return True
        else:
            # 回滚
            self.available += request
            self.allocation[pid] -= request
            self.need[pid] += request
            print("分配后系统不安全，分配失败，回滚。")
            return False

# 测试
if __name__ == "__main__":
    # 示例数据（来自教材）
    available = [3, 3, 2]
    max_matrix = [
        [7, 5, 3],
        [3, 2, 2],
        [9, 0, 2],
        [2, 2, 2],
        [4, 3, 3]
    ]
    allocation = [
        [0, 1, 0],
        [2, 0, 0],
        [3, 0, 2],
        [2, 1, 1],
        [0, 0, 2]
    ]

    banker = Banker(available, max_matrix, allocation)
    
    print("初始状态安全性检查：")
    safe, seq = banker.is_safe()
    print(f"安全：{safe}, 安全序列：{seq}")

    print("\n进程1请求 (1, 0, 2): ")
    banker.request_resources(1, [1, 0, 2])

    print("\n当前可用资源：", banker.available)
    print("已分配矩阵：\n", banker.allocation)
    print("需求矩阵：\n", banker.need)

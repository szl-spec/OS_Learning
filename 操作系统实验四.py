class MemoryManager:
    def __init__(self, total_size):
        self.total_size = total_size
        # 空闲分区表：每个元素为 (起始地址, 大小)
        self.free_blocks = [(0, total_size)]
        # 已分配记录：{进程名: (起始地址, 大小)}
        self.allocated = {}

    def show_free(self):
        """显示空闲分区表"""
        print("空闲分区表: ", self.free_blocks)

    def first_fit(self, name, size):
        """首次适应算法"""
        for i, (start, block_size) in enumerate(self.free_blocks):
            if block_size >= size:
                # 分配
                self.allocated[name] = (start, size)
                # 更新空闲分区
                if block_size == size:
                    del self.free_blocks[i]
                else:
                    self.free_blocks[i] = (start + size, block_size - size)
                print(f"进程 {name} 分配 {size}K 成功 (首次适应)")
                return True
        print(f"进程 {name} 分配失败, 无足够内存")
        return False

    def best_fit(self, name, size):
        """最佳适应算法"""
        best_idx = -1
        best_size = float('inf')
        for i, (start, block_size) in enumerate(self.free_blocks):
            if block_size >= size and block_size < best_size:
                best_idx = i
                best_size = block_size

        if best_idx != -1:
            start, block_size = self.free_blocks[best_idx]
            self.allocated[name] = (start, size)
            if block_size == size:
                del self.free_blocks[best_idx]
            else:
                self.free_blocks[best_idx] = (start + size, block_size - size)
            print(f"进程 {name} 分配 {size}K 成功 (最佳适应)")
            return True
        else:
            print(f"进程 {name} 分配失败, 无足够内存")
            return False

    def worst_fit(self, name, size):
        """最坏适应算法"""
        worst_idx = -1
        worst_size = -1
        for i, (start, block_size) in enumerate(self.free_blocks):
            if block_size >= size and block_size > worst_size:
                worst_idx = i
                worst_size = block_size

        if worst_idx != -1:
            start, block_size = self.free_blocks[worst_idx]
            self.allocated[name] = (start, size)
            if block_size == size:
                del self.free_blocks[worst_idx]
            else:
                self.free_blocks[worst_idx] = (start + size, block_size - size)
            print(f"进程 {name} 分配 {size}K 成功 (最坏适应)")
            return True
        else:
            print(f"进程 {name} 分配失败, 无足够内存")
            return False

    def release(self, name):
        """释放进程占用的内存"""
        if name not in self.allocated:
            print(f"进程 {name} 不存在")
            return

        start, size = self.allocated.pop(name)
        # 将释放的块插入空闲表，并合并相邻块
        self.free_blocks.append((start, size))
        # 按起始地址排序
        self.free_blocks.sort(key=lambda x: x[0])

        # 合并相邻空闲块
        i = 0
        while i < len(self.free_blocks) - 1:
            current_start, current_size = self.free_blocks[i]
            next_start, next_size = self.free_blocks[i + 1]
            if current_start + current_size == next_start:
                # 合并
                self.free_blocks[i] = (current_start, current_size + next_size)
                del self.free_blocks[i + 1]
            else:
                i += 1
        print(f"进程 {name} 释放内存，当前空闲表: {self.free_blocks}")


# 测试代码
if __name__ == "__main__":
    # --- 首次适应算法 ---
    print("=== 首次适应算法 ===")
    mm = MemoryManager(1024)
    mm.first_fit("A", 200)
    mm.show_free()
    mm.first_fit("B", 150)
    mm.show_free()
    mm.release("A")
    mm.show_free()
    mm.first_fit("C", 100)
    mm.show_free()

    # --- 最佳适应算法 ---
    print("\n=== 最佳适应算法 ===")
    mm2 = MemoryManager(1024)
    mm2.best_fit("A", 200)
    mm2.best_fit("B", 150)
    mm2.release("A")
    mm2.best_fit("C", 100)
    mm2.show_free()

    # --- 最坏适应算法 ---
    print("\n=== 最坏适应算法 ===")
    mm3 = MemoryManager(1024)
    mm3.worst_fit("A", 200)
    mm3.worst_fit("B", 150)
    mm3.release("A")
    mm3.worst_fit("C", 100)
    mm3.show_free()
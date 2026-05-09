"""
实验五：页面置换算法模拟（OPT, FIFO, LRU）
统计缺页次数和缺页率
"""


def opt(seq, frames):
    """***最佳置换算法***"""
    memory = []
    page_faults = 0
    for i, page in enumerate(seq):
        if page not in memory:
            page_faults += 1
            if len(memory) < frames:
                memory.append(page)
            else:
                # 选择未来最远使用或永不使用的页面置换
                future_use = []
                for p in memory:
                    if p in seq[i + 1:]:
                        idx = seq[i + 1:].index(p) + i + 1
                    else:
                        idx = float('inf')
                    future_use.append((p, idx))

                # 置换未来最远使用的
                to_replace = max(future_use, key=lambda x: x[1])[0]
                pos = memory.index(to_replace)
                memory[pos] = page

        # 输出当前内存状态
        print(f"访问 {page}: {memory}")
    return page_faults


def fifo(seq, frames):
    """***先进先出置换算法***"""
    memory = []
    page_faults = 0
    queue = []  # 用于记录进入顺序
    for i, page in enumerate(seq):
        if page not in memory:
            page_faults += 1
            if len(memory) < frames:
                memory.append(page)
                queue.append(page)
            else:
                # 移除队首
                removed = queue.pop(0)
                pos = memory.index(removed)
                memory[pos] = page
                queue.append(page)
        else:
            # 如果页面已经在内存中，FIFO 不调整顺序（队列不变）
            pass

        print(f"访问 {page}: {memory}")
    return page_faults


def lru(seq, frames):
    """***最近最久未使用置换算法***"""
    memory = []
    page_faults = 0
    # 使用列表记录最近使用顺序，尾部表示最近使用
    recent = []
    for i, page in enumerate(seq):
        if page not in memory:
            page_faults += 1
            if len(memory) < frames:
                memory.append(page)
                recent.append(page)
            else:
                # 置换最近最久未使用的，即 recent 头部
                lru_page = recent.pop(0)
                pos = memory.index(lru_page)
                memory[pos] = page
                recent.append(page)
        else:
            # 更新 recent，将当前页移到尾部
            recent.remove(page)
            recent.append(page)

        print(f"访问 {page}: {memory}")
    return page_faults


if __name__ == "__main__":
    # 页面访问序列
    seq = [7, 0, 1, 2, 0, 3, 0, 4, 2, 3, 0, 3, 2, 1, 2, 0, 1, 7, 0, 1]
    frames = 3

    print("页面访问序列：", seq)
    print("内存块数：", frames)

    print("\n--- OPT ---")
    faults = opt(seq, frames)
    print(f"缺页次数：{faults}，缺页率：{faults / len(seq):.2%}")

    print("\n--- FIFO ---")
    faults = fifo(seq, frames)
    print(f"缺页次数：{faults}，缺页率：{faults / len(seq):.2%}")

    print("\n--- LRU ---")
    faults = lru(seq, frames)
    print(f"缺页次数：{faults}，缺页率：{faults / len(seq):.2%}")
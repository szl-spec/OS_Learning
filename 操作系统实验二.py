"""
实验二：生产者-消费者问题（有界缓冲区）
使用 threading 模块模拟多线程同步
"""

import threading
import time
import random

# 缓冲区设置
BUFFER_SIZE = 5
buffer = []  # 共享缓冲区
mutex = threading.Lock()  # 互斥锁，保护对缓冲区的访问
empty = threading.Semaphore(BUFFER_SIZE)  # 空缓冲区数量
full = threading.Semaphore(0)  # 满缓冲区数量


# 生产者线程函数
def producer(id):
    for i in range(3):  # 每个生产者生产3次
        item = random.randint(1, 100)  # 生产一个产品
        empty.acquire()  # P(empty)，等待空缓冲区
        mutex.acquire()  # 进入临界区

        # 将产品放入缓冲区
        buffer.append(item)
        print(f"生产者 {id} 生产了产品 {item}，缓冲区：{buffer}")

        mutex.release()  # 退出临界区
        full.release()  # V(full)，增加满缓冲区计数
        time.sleep(random.uniform(0.5, 1.5))  # 模拟生产耗时


# 消费者线程函数
def consumer(id):
    for i in range(3):  # 每个消费者消费3次
        full.acquire()  # P(full)，等待产品
        mutex.acquire()  # 进入临界区

        # 从缓冲区取出产品
        item = buffer.pop(0)
        print(f"消费者 {id} 消费了产品 {item}，缓冲区：{buffer}")

        mutex.release()  # 退出临界区
        empty.release()  # V(empty)，增加空缓冲区计数
        time.sleep(random.uniform(0.5, 1.5))  # 模拟消费耗时


if __name__ == "__main__":
    # 创建 2 个生产者和 2 个消费者
    producers = [threading.Thread(target=producer, args=(i,)) for i in range(1, 3)]
    consumers = [threading.Thread(target=consumer, args=(i,)) for i in range(1, 3)]

    # 启动所有线程
    for t in producers + consumers:
        t.start()

    # 等待所有线程结束
    for t in producers + consumers:
        t.join()

    print("所有生产者和消费者执行完毕。")
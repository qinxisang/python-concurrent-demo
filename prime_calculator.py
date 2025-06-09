import threading
import time
import math


# 判断质数的函数
def is_prime(n):
    if n <= 1:
        return False
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True


# 线程工作函数
def calculate_primes(start, end, results):
    primes = []
    for num in range(start, end):
        if is_prime(num):
            primes.append(num)
    results.extend(primes)


# 单线程计算
def single_thread():
    results = []
    start_time = time.time()
    calculate_primes(1, 1000000, results)
    print(f"单线程耗时: {time.time() - start_time:.2f}秒, 找到{len(results)}个质数")


# 多线程计算
def multi_thread(thread_count=8):
    results = []
    threads = []
    chunk_size = 1000000 // thread_count

    start_time = time.time()
    for i in range(thread_count):
        start = i * chunk_size + 1
        end = (i + 1) * chunk_size if i < thread_count - 1 else 1000000
        t = threading.Thread(
            target=calculate_primes,
            args=(start, end, results)
        )
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    print(f"{thread_count}线程耗时: {time.time() - start_time:.2f}秒, 找到{len(results)}个质数")


if __name__ == "__main__":
    print(":: 质数计算性能测试 ::")
    single_thread()
    multi_thread()
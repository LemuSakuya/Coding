#1
import threading
import time
import random
from queue import Queue

queue = Queue(maxsize=3)

class Producer(threading.Thread):
    def run(self):
        global queue
        while True:
            time.sleep(random.uniform(0.1, 0.5))
            item = f"商品-{time.time()}"
            if queue.full():
                print(f"队列已满，生产者等待...")
            queue.put(item)
            print(f"生产者生产: {item} (队列大小: {queue.qsize()})")

class Consumer(threading.Thread):
    def run(self):
        global queue
        while True:            
            time.sleep(random.uniform(0.5, 1))
            if queue.empty():
                print(f"队列为空，消费者等待...")
            item = queue.get()
            print(f"消费者消费: {item} (队列大小: {queue.qsize()})")
            queue.task_done()

if __name__ == "__main__":
    print("启动生产者和消费者线程...")
    print("队列最大容量: 3")
    
    producer = Producer()
    consumer = Consumer()
    
    producer.daemon = True
    consumer.daemon = True
    
    producer.start()
    consumer.start()

    try:    
        while True:
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("\n程序结束")

# # #2
# import random
# import time
# import multiprocessing
# import threading
# from multiprocessing import Pool

# def monte_carlo_pi_part(n):
#     count = 0
#     for _ in range(n):
#         x = random.random()
#         y = random.random()
#         if x**2 + y**2 <= 1:
#             count += 1
#     return count

# def single_process(total_samples):
#     start_time = time.time()
#     count = monte_carlo_pi_part(total_samples)
#     pi = 4 * count / total_samples
#     end_time = time.time()
#     print(f"单进程结果: π ≈ {pi:.8f}, 耗时: {end_time - start_time:.4f}秒")
#     return end_time - start_time

# def worker_function(n, q):
#     q.put(monte_carlo_pi_part(n))

# def multi_process_no_pool(total_samples, num_processes):
#     start_time = time.time()
#     samples_per_process = total_samples // num_processes
#     processes = []
#     result_queue = multiprocessing.Queue()
    
#     for _ in range(num_processes):
#         p = multiprocessing.Process(
#             target=worker_function,
#             args=(samples_per_process, result_queue)
#         )
#         processes.append(p)
#         p.start()
    
#     for p in processes:
#         p.join()
    
#     results = []
#     while not result_queue.empty():
#         results.append(result_queue.get())
    
#     count = sum(results)
#     pi = 4 * count / (samples_per_process * num_processes)
#     end_time = time.time()
#     print(f"多进程(无池)结果: π ≈ {pi:.8f}, 耗时: {end_time - start_time:.4f}秒")
#     return end_time - start_time

# def multi_process_with_pool(total_samples, num_processes):
#     start_time = time.time()
#     samples_per_process = total_samples // num_processes
    
#     with Pool(num_processes) as pool:
#         results = pool.map(monte_carlo_pi_part, [samples_per_process] * num_processes)
    
#     count = sum(results)
#     pi = 4 * count / (samples_per_process * num_processes)
#     end_time = time.time()
#     print(f"多进程(有池)结果: π ≈ {pi:.8f}, 耗时: {end_time - start_time:.4f}秒")
#     return end_time - start_time

# def multi_thread(total_samples, num_threads):
#     start_time = time.time()
#     samples_per_thread = total_samples // num_threads
#     threads = []
#     results = [0] * num_threads  # 用于存储结果的列表
    
#     def worker(thread_idx, n):
#         results[thread_idx] = monte_carlo_pi_part(n)
    
#     for i in range(num_threads):
#         t = threading.Thread(target=worker, args=(i, samples_per_thread))
#         threads.append(t)
#         t.start()
    
#     for t in threads:
#         t.join()
    
#     count = sum(results)
#     pi = 4 * count / (samples_per_thread * num_threads)
#     end_time = time.time()
#     print(f"多线程结果: π ≈ {pi:.8f}, 耗时: {end_time - start_time:.4f}秒")
#     return end_time - start_time

# def compare_methods(total_samples=1000000, max_workers=4):
#     print(f"总样本数: {total_samples}, 最大工作进程/线程数: {max_workers}")
    
#     times = {
#         "单进程": single_process(total_samples),
#     }
    
#     for workers in range(2, max_workers + 1):
#         print(f"\n使用 {workers} 个工作进程/线程:")
#         times[f"多进程(无池)-{workers}"] = multi_process_no_pool(total_samples, workers)
#         times[f"多进程(有池)-{workers}"] = multi_process_with_pool(total_samples, workers)
#         times[f"多线程-{workers}"] = multi_thread(total_samples, workers)
    
#     print("\n效率比较:")
#     for method, t in sorted(times.items(), key=lambda x: x[1]):
#         print(f"{method}: {t:.4f}秒")

# if __name__ == "__main__":
#     multiprocessing.freeze_support()  # 在Windows上可能需要这一行
#     compare_methods(total_samples=1000000, max_workers=4)

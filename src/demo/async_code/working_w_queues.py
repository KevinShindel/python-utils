from asyncio import Queue, PriorityQueue, LifoQueue
import asyncio
from random import uniform
import time
import random


async def worker(name, queue):
    while True:
        # Get a "work item" out of the queue.
        sleep_for = await queue.get()

        # Sleep for the "sleep_for" seconds.
        await asyncio.sleep(sleep_for)

        # Notify the queue that the "work item" has been processed.
        queue.task_done()

        print(f'{name} has slept for {sleep_for:.2f} seconds')


async def queue_main():
    # Create a queue that we will use to store our "workload".
    queue = Queue()

    # Generate random timings and put them into the queue.
    total_sleep_time = 0
    for _ in range(20):
        sleep_for = uniform(0.05, 1.0)
        total_sleep_time += sleep_for
        queue.put_nowait(sleep_for)

    # Create three worker tasks to process the queue concurrently.
    tasks = []
    for i in range(3):
        task = asyncio.create_task(worker(f'worker-{i}', queue))
        tasks.append(task)

    # Wait until the queue is fully processed.
    started_at = time.monotonic()
    await queue.join()
    total_slept_for = time.monotonic() - started_at

    # Cancel our worker tasks.
    for task in tasks:
        task.cancel()
    # Wait until all worker tasks are cancelled.
    await asyncio.gather(*tasks, return_exceptions=True)

    print('====')
    print(f'3 workers slept in parallel for {total_slept_for:.2f} seconds')
    print(f'total expected sleep time: {total_sleep_time:.2f} seconds')


def lifo_queue():
    queue = LifoQueue()
    queue.put_nowait(10)
    queue.put_nowait(20)
    queue.put_nowait(30)
    assert queue.get_nowait() == 30  # must return the last message from queue


def priority_queue():
    queue = PriorityQueue()

    queue.put_nowait((4, {'some4': 'value4'}))
    queue.put_nowait((1, {'some': 'value1'}))
    queue.put_nowait((2, {'some2': 'value2'}))

    data = queue.get_nowait()
    assert data == (1, {'some': 'value1'})  # must return 1 by ordering the queue


async def producer(queue, producer_id, num_items):
    """A producer that puts items into the queue."""
    for i in range(num_items):
        # Simulate producing an item
        await asyncio.sleep(random.uniform(0.1, 0.5))
        item = f"Producer-{producer_id}-Item-{i}"
        await queue.put(item)
        print(f"[Producer {producer_id}] Produced: {item}")
    print(f"[Producer {producer_id}] Finished producing {num_items} items.")


async def consumer(queue, consumer_id):
    """A consumer that takes items from the queue and processes them."""
    while True:
        item = await queue.get()  # Wait until an item is available
        # Process the item
        print(f"[Consumer {consumer_id}] Consumed: {item}")
        await asyncio.sleep(random.uniform(0.2, 1.0))  # Simulate processing time
        queue.task_done()  # Indicate the item has been processed


async def main():
    queue = asyncio.Queue()  # Shared queue
    num_producers = 12  # Number of producers
    num_consumers = 3  # Number of consumers
    num_items_per_producer = 5

    # Create producer tasks
    producers = [
        asyncio.create_task(producer(queue, i, num_items_per_producer))
        for i in range(num_producers)
    ]

    # Create consumer tasks
    consumers = [
        asyncio.create_task(consumer(queue, i))
        for i in range(num_consumers)
    ]

    # Wait for all producers to finish producing
    await asyncio.gather(*producers)

    # Wait for the queue to become empty (all items processed)
    await queue.join()

    # Cancel all consumers since they run indefinitely
    for c in consumers:
        c.cancel()
    await asyncio.gather(*consumers, return_exceptions=True)


# Run the program
asyncio.run(main())

if __name__ == '__main__':
    # asyncio.run(queue_main())
    # lifo_queue()
    # priority_queue()
    asyncio.run(main())

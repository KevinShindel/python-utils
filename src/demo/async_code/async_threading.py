# Workload Type	Executor to Use	Reason
# I/O-bound tasks	ThreadPoolExecutor	Threads work well with blocking I/O and avoid the overhead of processes.
# CPU-bound tasks	ProcessPoolExecutor	Processes bypass the GIL, enabling true parallelism for heavy computations.
# Mixed workload	Hybrid Approach	Use a combination: asyncio for I/O; ProcessPoolExecutor for CPU tasks.

# with GIL
import asyncio
from concurrent.futures import ThreadPoolExecutor

def blocking_function(n):
    # Some computationally expensive blocking operation
    print("Starting blocking operation")
    result = sum(range(n))
    print("Blocking operation complete")
    return result

async def main():
    loop = asyncio.get_event_loop()
    with ThreadPoolExecutor() as executor:
        # Run blocking code in a separate thread
        result = await loop.run_in_executor(executor, blocking_function, 10**6)
        print(f"Result: {result}")

asyncio.run(main())

# without GIL
import asyncio
from concurrent.futures import ProcessPoolExecutor

def cpu_bound_task(n):
    # Intensive computation
    return sum(i * i for i in range(n))

async def main():
    loop = asyncio.get_event_loop()
    with ProcessPoolExecutor() as executor:
        # Offload CPU-bound task to a separate process
        result = await loop.run_in_executor(executor, cpu_bound_task, 10**7)
        print(f"Result: {result}")

asyncio.run(main())

# run a list of async tasks

import asyncio
from concurrent.futures import ProcessPoolExecutor


def cpu_bound_task(n):
    # Simulate an expensive computation (e.g., sum of squares)
    return sum(i * i for i in range(n))


async def main():
    loop = asyncio.get_event_loop()
    tasks = []

    # Create a process pool with concurrent.futures.ProcessPoolExecutor
    with ProcessPoolExecutor() as executor:
        # Prepare data for multiple CPU-bound tasks
        args_list = [10 ** 6, 10 ** 7, 10 ** 8]  # Payload for each task

        for args in args_list:
            # Use loop.run_in_executor to offload CPU tasks to the process pool
            tasks.append(
                loop.run_in_executor(
                    executor, cpu_bound_task, args
                )
            )

        # Wait for the tasks to complete
        results = await asyncio.gather(*tasks)

    # Print the results
    for i, result in enumerate(results):
        print(f"Task {i + 1} result: {result}")


# Run the async main function
asyncio.run(main())

# Combination asyncio & ThreadPoolExecutor & ProcessPoolExecutor
import asyncio
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor


# Example functions
def cpu_bound_task(n):
    return sum(i * i for i in range(n))


def io_bound_task(n):
    return sum([x for x in range(n)])


async def main():
    loop = asyncio.get_event_loop()

    # Use ThreadPoolExecutor for I/O tasks
    with ThreadPoolExecutor() as thread_executor, ProcessPoolExecutor() as process_executor:
        io_tasks = [loop.run_in_executor(thread_executor, io_bound_task, 10**6) for _ in range(5)]
        cpu_tasks = [loop.run_in_executor(process_executor, cpu_bound_task, 10**6) for _ in range(5)]

        # Gather results for both concurrently
        results = await asyncio.gather(*io_tasks, *cpu_tasks)
        print(results)


asyncio.run(main())



# Real-World Use Case: Handling File I/O and Network API Coordination
# Imagine you're creating a data processing application that interacts with a web API to fetch data and then performs some intensive,
# blocking file I/O operations, like compressing retrieved data or converting large images.
# The network tasks can be handled asynchronously using asyncio,
# but file processing is blocking and benefits from threads (using ThreadPoolExecutor).
import asyncio
from concurrent.futures import ThreadPoolExecutor
import requests
import time

# Blocking function for file processing (CPU-bound or I/O-heavy)
def process_file(file_path):
    print(f"Starting file processing: {file_path}")
    time.sleep(3)  # Simulating a blocking operation (e.g., compression, image processing)
    print(f"Finished file processing: {file_path}")
    return f"Processed {file_path}"

# Asynchronous function for downloading data using requests in threads
async def fetch_data(session, url):
    loop = asyncio.get_event_loop()
    print(f"Fetching data from: {url}")
    response = await loop.run_in_executor(None, lambda: session.get(url))
    print(f"Finished fetching data from: {url}")
    return response.text

async def process_data_with_thread_pool(file_paths, executor):
    loop = asyncio.get_event_loop()
    tasks = []
    for file_path in file_paths:
        # Submit file processing tasks to the ThreadPoolExecutor
        tasks.append(loop.run_in_executor(executor, process_file, file_path))
    return await asyncio.gather(*tasks)

async def main():
    urls = [
        "https://example.com/data1",
        "https://example.com/data2",
        "https://example.com/data3",
    ]
    file_paths = ["file1.txt", "file2.txt", "file3.txt"]

    # Create a ThreadPoolExecutor for file processing tasks
    with ThreadPoolExecutor(max_workers=3) as executor:
        async with asyncio.Semaphore(3):  # Limit the number of concurrent downloads
            async with requests.Session() as session:
                # Fetch data asynchronously
                fetch_tasks = [fetch_data(session, url) for url in urls]
                downloaded_data = await asyncio.gather(*fetch_tasks)

                print(f"Downloaded data: {downloaded_data}")

                # Process files in a thread pool, concurrently with asyncio's event loop
                processed_files = await process_data_with_thread_pool(file_paths, executor)
                print(f"Processed files: {processed_files}")

# Run the asyncio event loop
asyncio.run(main())
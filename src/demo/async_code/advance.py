import asyncio
import time


async def say_after(delay: int, content: str):
    await asyncio.sleep(delay)
    print(content)
    return delay ** 2


async def main():
    async with asyncio.TaskGroup() as tg:  # Tasks are used to schedule coroutines concurrently.
        task1 = tg.create_task(
            say_after(1, 'hello'))

        task2 = tg.create_task(
            say_after(0.5, 'world'))

        print(f"started at {time.strftime('%X')}")

    # To await is implicit when the context manager exits.
    print(f"Both tasks have completed now: {task1.result()}, {task2.result()}")
    print(f"finished at {time.strftime('%X')}")


# Running Tasks Concurrently
async def concurrent_run():
    # Note If return_exceptions is false, cancelling gather() after it has been marked done won’t cancel any submitted awaitables.
    # For instance, gather can be marked done after propagating an exception to the caller, therefore,
    # calling gather.cancel() after catching an exception (raised by one of the awaitables) from gather won’t cancel any other awaitables.
    async def factorial(name, number):
        f = 1
        for i in range(2, number + 1):
            print(f"Task {name}: Compute factorial({number}), currently i={i}...")
            await asyncio.sleep(1)
            f *= i
        print(f"Task {name}: factorial({number}) = {f}")
        return f

    # Schedule three calls *concurrently*:
    L = await asyncio.gather(
        factorial("A", 2),
        factorial("B", 3),
        factorial("C", 4),
    )
    print(L)


# Shielding From Cancellation
async def shield_task():
    task = asyncio.create_task(say_after(1, 'shield'))
    try:
        res = await asyncio.shield(task)  # Protect an awaitable object from being cancelled.
    except asyncio.CancelledError:
        res = None
    return res


# Timeouts
# - asyncio.timeout
# - reschedule
# - asyncio.timeout_at
# - asyncio.wait_for
#


async def timeout_main():
    try:
        async with asyncio.timeout(10):
            await say_after(11, 'timeout')
    except TimeoutError:
        print("The long operation timed out, but we've handled it.")

    print("This statement will run regardless.")


async def main():
    try:
        # We do not know the timeout when starting, so we pass ``None``.
        async with asyncio.timeout(None) as cm:
            # We know the timeout now, so we reschedule it.
            new_deadline = asyncio.get_running_loop().time() + 10
            cm.reschedule(new_deadline)

            await say_after(11, 'timeout')
    except TimeoutError:
        pass

    if cm.expired():
        print("Looks like we haven't finished on time.")


# Waiting Primitives

aws = []
# done, pending = await asyncio.wait(aws) # Returns two sets of Tasks/Futures: (done, pending).
# async asyncio.wait(aws, *, timeout=None, return_when=ALL_COMPLETED)
# asyncio.FIRST_COMPLETED The function will return when any future finishes or is cancelled.
# asyncio.FIRST_EXCEPTION The function will return when any future finishes by raising an exception.
# If no future raises an exception then it is equivalent to ALL_COMPLETED.
# asyncio.ALL_COMPLETED The function will return when all futures finish or are cancelled.

asyncio.as_completed(aws, *[],
                     timeout=None)  # Run awaitable objects in the aws iterable concurrently. The returned object can be iterated to obtain the results of the awaitables


# as they finish.

def open_connection(ip, port):
    pass


ipv4_connect = asyncio.create_task(open_connection("127.0.0.1", 80))
ipv6_connect = asyncio.create_task(open_connection("::1", 80))
tasks = [ipv4_connect, ipv6_connect]


# Running in Threads
# async asyncio.to_thread(func, /, *args, **kwargs) # Asynchronously run function func in a separate thread

def blocking_io():
    print(f"start blocking_io at {time.strftime('%X')}")
    # Note that time.sleep() can be replaced with any blocking
    # IO-bound operation, such as file operations.
    time.sleep(1)
    print(f"blocking_io complete at {time.strftime('%X')}")


async def main():
    print(f"started main at {time.strftime('%X')}")

    await asyncio.gather(
        asyncio.to_thread(blocking_io),
        asyncio.sleep(1))

    print(f"finished main at {time.strftime('%X')}")


asyncio.run(main())

# Expected output:
#
# started main at 19:50:53
# start blocking_io at 19:50:53
# blocking_io complete at 19:50:54
# finished main at 19:50:54

# Directly calling blocking_io() in any coroutine would block the event loop for its duration,
# resulting in an additional 1 second of run time.
# Instead, by using asyncio.to_thread(), we can run it in a separate thread without blocking the event loop.

# Scheduling From Other Threads
coro = asyncio.sleep(1, result=3)
loop = asyncio.get_event_loop()
future = asyncio.run_coroutine_threadsafe(coro, loop)  # Submit a coroutine to the given event loop. Thread-safe.
timeout = 1

try:
    result = future.result(timeout)
except TimeoutError:
    print('The coroutine took too long, cancelling the task...')
    future.cancel()
except Exception as exc:
    print(f'The coroutine raised an exception: {exc!r}')
else:
    print(f'The coroutine returned: {result!r}')

# Introspection
asyncio.current_task(loop=None)  # Return the currently running Task instance, or None if no task is running.
asyncio.all_tasks(loop=None)  # Return a set of not yet finished Task objects run by the loop.
obj = future.result()
asyncio.iscoroutine(obj)  # Return True if obj is a coroutine object.


def callback_function(_obj):
    pass


# Task Object
task = asyncio.Task(coro, *[], loop=None, name=None,
                    context=None)  # A Future-like object that runs a Python coroutine. Not thread-safe.
task.done()  # Return True if the Task is done.
task.cancel()  # Canceling task
task.result()  # return result of the task
task.exception()  # Return the exception of the Task.
task.add_done_callback(callback_function)  # Add a callback to be run when the Task is done.
task.remove_done_callback(callback_function)  # Remove callback from the callbacks list.
task.get_stack()  # Return the list of stack frames for this Task.
task.print_stack()  # Print the stack or traceback for this Task.
task.get_coro()  # Return the coroutine object wrapped by the Task.
task.get_context()  # Return the contextvars.Context object associated with the task.
task.get_name()  # Return the name of the Task.
task.set_name()  # Return the name of the Task. \ Set the name of the Task.
task.cancelled()  # Return True if the Task is cancelled.

if __name__ == '__main__':
    # asyncio.run(main())
    asyncio.run(concurrent_run())

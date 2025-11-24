import asyncio


async def simple():
    print('Hello ...')
    await asyncio.sleep(1)
    print('... World!')


async def say_after(delay, content):
    await asyncio.sleep(delay)
    print(content)


async def main():
    task1 = asyncio.create_task(
        say_after(1, 'hello'))
    await task1

    task2 = asyncio.create_task(
        say_after(2, 'hello 2'))
    await task2


if __name__ == '__main__':
    asyncio.run(
        simple())  # This function cannot be called when another asyncio event loop is running in the same thread.

    # Runner context manager

    with asyncio.Runner() as runner:  # A context manager that simplifies multiple async function calls in the same context.
        runner.run(main())
        loop = runner.get_loop()

    asyncio.run(main())

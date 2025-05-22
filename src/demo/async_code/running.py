import asyncio

# Runners
if __name__ == '__main__':

    coro = asyncio.sleep(1)
    asyncio.run(coro, debug=True)

# Runner context manager
# A context manager that simplifies multiple async function calls in the same context.
# Sometimes several top-level async functions should be called in the same event loop and contextvars.Context.
async def main():
    await asyncio.sleep(1)
    print('hello')

with asyncio.Runner() as runner:
    runner.run(main())
    loop = runner.get_loop()
    runner.close()
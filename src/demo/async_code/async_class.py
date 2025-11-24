import asyncio


async def sample_function(item):
    await asyncio.sleep(1)
    print(f"Processed: {item}")
    return {"item": item}


class MultiAsyncExecute:

    def __init__(self, fn, iterable_objects):
        self.fn = fn
        self.items = iterable_objects

    async def __call__(self):
        # Create and yield tasks as they are generated
        for item in self.items:
            yield asyncio.create_task(self.fn(item), name=item)

    async def _execute(self):
        # Consume tasks one by one and yield their results
        async for task in self():
            yield await task  # Await the task and yield its result

    def run(self):
        # Use asyncio.run() to consume results from the async generator
        async def gather_results():
            _results = []
            async for result in self._execute():
                _results.append(result)  # Collect results lazily
            return results

        return asyncio.run(gather_results())


if __name__ == '__main__':
    # Instantiate the class and call the run method
    executor = MultiAsyncExecute(sample_function, ["item1", "item2", "item3"])
    results = executor.run()
    print("Results:", results)

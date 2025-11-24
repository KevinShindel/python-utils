from functools import cached_property  # Requires Python 3.8 or newer


class MyClass:
    def __init__(self, value):
        self.value = value

    @cached_property
    def expensive_computation(self):
        print("Performing expensive computation...")
        # Simulate a costly operation by squaring the value
        result = self.value ** 2
        return result


if __name__ == '__main__':
    # Create an instance of MyClass
    obj = MyClass(10)

    # Access the cached property
    print("First access:", obj.expensive_computation)  # Performs computation
    print("Second access:", obj.expensive_computation)  # Retrieves cached value

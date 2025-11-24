def my_decorator(*decorator_args, **decorator_kwargs):
    def decorator(func):
        def wrapper(*args, **kwargs):
            # Process the decorator's arguments and kwargs
            print(f"Decorator arguments: {decorator_args}")
            print(f"Decorator keyword arguments: {decorator_kwargs}")

            print("Function is about to be called.")
            result = func(*args, **kwargs)  # Call the target function
            print("Function call completed.")
            return result

        return wrapper

    return decorator


# Using the decorator with arguments and kwargs
@my_decorator(42, "Hello", verbose=True, mode="test")
def my_function(name):
    print(f"Hello, {name}!")


# Call the decorated function
my_function("Alice")

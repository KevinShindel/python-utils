class MyClass:
    def __init__(self, name):
        self.name = name

    def method_wrapper(func):
        """
        A static method decorator to wrap methods inside the class.
        """

        def wrapper(self, *args, **kwargs):
            print(f"Before calling '{func.__name__}'")
            print(f"Working on: {self.name}")

            result = func(self, *args, **kwargs)  # Call the original method

            print(f"After calling '{func.__name__}'")
            return result

        return wrapper

    @method_wrapper  # Apply the wrapper decorator
    def my_method(self, greeting):
        print(f"{greeting}, {self.name}!")

if __name__ == '__main__':

    # Create an instance of MyClass
    obj = MyClass("Alice")

    # Call the wrapped method
    obj.my_method("Hello")
import threading
import functools
import time

def stoppable(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        stop_event = threading.Event()
        def stop():
            return stop_event.is_set()

        # Insert the 'stop' function into the keyword arguments
        kwargs['stop'] = stop

        # Create and start the thread
        thread = threading.Thread(target=func, args=args, kwargs=kwargs)
        thread.stop = stop_event.set  # Add a stop method to the thread
        thread.start()
        return thread

    return wrapper

# Example usage with additional arguments
# @stoppable
# def my_function(arg1, arg2, stop):
#     while not stop():
#         print(f"Function is running with arguments: {arg1}, {arg2}")
#         time.sleep(1)
#     print("Function is stopping")

# # Start the function in a thread with additional arguments
# thread = my_function("Hello", "World")

# # Stop the function after some time
# time.sleep(5)
# thread.stop()
# thread.join()
# print("Thread has stopped")
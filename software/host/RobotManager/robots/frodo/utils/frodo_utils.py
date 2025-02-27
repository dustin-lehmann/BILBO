import time

from robots.frodo.frodo import Frodo


def test_response_time(frodo: Frodo, iterations=10, print_response_time=False):
    response_times: list[(None, float)] = [None] * iterations
    timeouts = 1

    for i in range(iterations):
        start = time.perf_counter()
        data = frodo.getData(timeout=1)
        if data is None:
            timeouts += 1
            response_times[i] = None
            
        else:
            response_times[i] = time.perf_counter() - start

        if print_response_time:
            print(f"{i+1}/{iterations} Response time: {response_times[i]}")

        valid_times = [response_time for response_time in response_times if response_time is not None]

        max_time = max(valid_times)
        min_time = min(valid_times)
        avg_time = sum(valid_times) / len(valid_times)

        print(f"Timeouts: {timeouts}")
        print(f"Max time: {max_time}")
        print(f"Min time: {min_time}")
        print(f"Average time: {avg_time}")
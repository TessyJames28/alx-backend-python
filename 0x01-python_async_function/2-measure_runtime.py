#!/usr/bin/env python3
"""function that measure the runtime"""
import time
import asyncio
wait_n = __import__('1-concurrent_coroutines').wait_n


def measure_time(n: int, max_delay: int) -> float:
    """measures the total execution time for wait_n(n, max_delay)"""
    s_time = time.time()
    asyncio.run(wait_n(n, max_delay))
    e_time = time.time()
    total_time = e_time - s_time
    return total_time / n

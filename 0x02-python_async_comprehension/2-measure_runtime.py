#!/usr/bin/env python3
"""execute async_comprehension 4 times in parallel using asyncio.gather"""
from typing import Generator
import asyncio
import time
async_comprehension = __import__('1-async_comprehension').async_comprehension


async def measure_runtime() -> float:
    """measure the total runtime and return it"""
    s_time = time.time()
    task = [asyncio.create_task(async_comprehension()) for x in range(4)]
    await asyncio.gather(*task)
    e_time = time.time()
    t_time = e_time - s_time
    return t_time

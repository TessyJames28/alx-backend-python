#!/usr/bin/env python3
"""Execute a multiple coroutine at the same time with async"""
from typing import List
import asyncio
task_wait_random = __import__('3-tasks').task_wait_random


async def task_wait_n(n: int, max_delay: int) -> List[float]:
    """returns a list of all the delays"""
    val_list = []
    for num in range(n):
        val_list.append(task_wait_random(max_delay))

    result = await asyncio.gather(*val_list)
    return sorted(result)

#!/usr/bin/env python3
"""Execute a multiple coroutine at the same time with async"""
from typing import List
wait_random = __import__('0-basic_async_syntax').wait_random


async def wait_n(n: int, max_delay: int) -> List[float]:
    """returns a list of all the delays"""
    val_list = []
    for num in range(n):
        value = await wait_random(max_delay)
        val_list.append(value)
    return sorted(val_list)

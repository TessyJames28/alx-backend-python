#!/usr/bin/env python3
"""Basic async in python"""
import asyncio
import random


async def wait_random(max_delay: int = 10) -> float:
    """ The function tasks an int and returns a random float value """
    value = random.uniform(0, max_delay)
    await asyncio.sleep(value)
    return value

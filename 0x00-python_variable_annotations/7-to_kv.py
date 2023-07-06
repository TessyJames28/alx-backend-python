#!/usr/bin/env python3
""" function that handle complex type annotation str and int/float to tuple """
from typing import Union, Tuple


def to_kv(k: str, v: Union[int, float]) -> Tuple[str, float]:
    """ handles complex types """
    return k, v ** 2

#!/usr/bin/env python3
""" function that accepts mixed list based on complex Types """
from typing import List, Union


def sum_mixed_list(mxd_lst: List[Union[int, float]]) -> float:
    """Sums the int and float value and return a float
    """
    return sum(mxd_lst)

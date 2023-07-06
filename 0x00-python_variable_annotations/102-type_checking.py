#!/usr/bin/env python3
""" Module 12 - Type Checking """
from typing import List, Tuple, Any


def zoom_array(lst: Tuple, factor: int = 2) -> List:
    """ Return zoomed_in array """
    zoomed_in: List = [
        item for item in lst
        for i in range(factor)
    ]
    return zoomed_in


array: Tuple = (12, 72, 91)

zoom_2x: List = zoom_array(array)

zoom_3x: List = zoom_array(array, 3)

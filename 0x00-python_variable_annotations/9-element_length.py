#!/usr/bin/env python3
"""
Annotate the function’s parameters & return values with the appropriate type
"""
from typing import Sequence, Iterable, Tuple, List


def element_length(lst: Iterable[Sequence]) -> List[Tuple[Sequence, int]]:
    """ returns values with appropriate types """
    return [(i, len(i)) for i in lst]

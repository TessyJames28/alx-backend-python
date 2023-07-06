#!/usr/bin/env python3
"""More involved type annotations"""
from typing import TypeVar, Union, Any, Mapping


T = TypeVar('T')


def safely_get_value(dct: Mapping, key: Any,
                     default: Union[T, None] = None) -> Union[Any, T]:
    """ returns key if key in dct """
    if key in dct:
        return dct[key]
    else:
        return default

from __future__ import annotations
from collections.abc import Callable
from typing import Any

# Type definitions

type Container = Any

# Code

def quick_sort(
        container: Container,
        less: Callable[[Container, int, int], bool],
        swap: Callable[[Container, int, int], Container],
        end: int,
        begin: int = 0
) -> Container:
    """
    Sorts a container in place using the quicksort algorithm (three-way partitioning for duplicates).

    Args:
        container (Container): The container to be sorted. No constraints are put on the container as long as the `less` and `swap` methods are defined for it.
        less (Callable[[Container, int, int], bool]): A function that compares two items in the Container and returns True if the first is less than the second.
        swap (Callable[[Container, int, int], Container]): A function that swaps two items in the Container signified by their index positions.
        end (int): The ending index (one-past-the-last-element) of the portion of the Container to sort. Shall be typically set to the len of the Container at the first call.
        begin (int): The starting index of the portion of the list to sort. Defaults to 0.

    Return:
        Container: `container` after sorted
    """

    last = end-1

    def partition3(container, less, swap, last, begin):
        pivot = last
        lt = begin
        i = begin
        gt = last
        while i <= gt:
            if less(container, i, pivot):
                swap(container, lt, i)
                lt += 1
                i += 1
            elif less(container, pivot, i):
                swap(container, i, gt)
                gt -= 1
            else:
                i += 1
        return lt, gt

    if begin < last:
        lt, gt = partition3(container, less, swap, last, begin)
        quick_sort(container, less, swap, lt, begin)
        quick_sort(container, less, swap, end, gt + 1)

    return container


# selection sort is preferred over bubble sort as it results in less swaps in general
def selection_sort_step(
        container: Container,
        less: Callable[[Container, int, int], bool],
        swap: Callable[[Container, int, int], Container],
        end: int,
        begin: int = 0
):
    """
    Finds the lowest element in the container and swaps it with the element at `begin`.

    To be consecutively called with `begin = 0..(len-1)`,
    which effectively implements the selection sort algorithm.

    This is the least optimal way of sorting but it allows for
    easy progress-bar implementation...

    Args:
        container (Container): The container to be sorted. No constraints are put on the container as long as the `less` and `swap` methods are defined for it.
        less (Callable[[Container, int, int], bool]): A function that compares two items in the Container and returns True if the first is less than the second.
        swap (Callable[[Container, int, int], Container]): A function that swaps two items in the Container signified by their index positions.
        end (int): The ending index (one-past-the-last-element) of the portion of the Container to sort. Shall be typically set to the len of the Container at the first call.
        begin (int): The starting index of the portion of the list to sort. Defaults to 0.

    Return:
        Container: `container` after sorted
    """

    def find_min() -> int:
        result = begin
        for i in range(begin+1, end):
            if less(container, i, result): result = i
        return result
    
    return swap(container, begin, find_min())


def is_blank(record: str|None) -> bool:
    """
    Identify if record is a blank sample

    Args:
        record (str|None): the record name to inspect

    Returns:
        bool: True if the record name includes "blank" (case insensitive)
    """

    return False if record is None else "blank" in record.casefold()



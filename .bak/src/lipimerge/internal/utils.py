from __future__ import annotations
from collections.abc import Callable
from typing import Any

# Type definitions

type Container = Any

# Code

# # In-place Quick Sort (thanks GitHub copilot :))
def quick_sort(
        container: Container,
        less: Callable[[Container, int, int], bool],
        swap: Callable[[Container, int, int], None],
        end: int,
        begin: int = 0
) -> Container:
    """
    Sorts a container in place using the quicksort algorithm (three-way partitioning for duplicates).

    Args:
        container (Container): The container to be sorted. No constraints are put on the container as long as the `less` and `swap` methods are defined for it.
        less (Callable[[Container, int, int], bool]): A function that compares two items in the Container and returns True if the first is less than the second.
        swap (Callable[[Container, int, int], None]): A function that swaps two items in the Container signified by their index positions.
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

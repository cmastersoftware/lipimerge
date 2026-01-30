import pytest
from lipimerge.internal.utils import quick_sort
from lipimerge.internal.utils import selection_sort_step

@pytest.mark.parametrize("array", [
    [], [1], [5, 5, 5, 5],
    [2, 1], [3, 1, 2], [1, 3, 2],
    [1, 2, 3, 4, 5], [10, 20, 30, 40, 50],
    [5, 4, 3, 2, 1], [50, 40, 30, 20, 10],
    [3, 6, 8, 10, 1, 2, 1], [5, 2, 9, 1, 5, 6], [9, 7, 5, 11, 12, 6, 2],
    [4, -1, 0, -1, 3, 4], [10, -10, 0, 5, -5, 10],
])
def test_quick_sort_default(array):
    expected = sorted(array)
    copy = list(array)  # prevent modifying the original
    
    def less(arr, i, j):
        return arr[i] < arr[j]
    
    def swap(arr, i, j):
        arr[i], arr[j] = arr[j], arr[i]
        return arr

    assert quick_sort(copy, less=less, swap=swap, end=len(copy)) == expected

@pytest.mark.parametrize("array", [
    [], [1], [5, 5, 5, 5],
    [2, 1], [3, 1, 2], [1, 3, 2],
    [1, 2, 3, 4, 5], [10, 20, 30, 40, 50],
    [5, 4, 3, 2, 1], [50, 40, 30, 20, 10],
    [3, 6, 8, 10, 1, 2, 1], [5, 2, 9, 1, 5, 6], [9, 7, 5, 11, 12, 6, 2],
    [4, -1, 0, -1, 3, 4], [10, -10, 0, 5, -5, 10],
])
def test_selection_sort(array):
    expected = sorted(array)
    copy = list(array)  # prevent modifying the original
    
    def less(arr, i, j):
        return arr[i] < arr[j]
    
    def swap(arr, i, j):
        arr[i], arr[j] = arr[j], arr[i]
        return arr
    
    for i in range(len(array)-1):
        selection_sort_step(array, less=less, swap=swap, end=len(array), begin=i)

    assert array == expected


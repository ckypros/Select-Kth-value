from typing import List, TypeVar
import random
import time
import math
import sys

# Warning, this can cause page fault issues modifying the recursion limit
# This change was carefully implemented to test larger values of n 
sys.setrecursionlimit(20000)

# T is a type var to represent a data type of an array passed to any of the algorithms
T = TypeVar('T')

# Quick sort is used to implement the quick sort algorithm parameters to sort the array
def quick_sort(array: List[T]) -> None:
    perform_quick_sort(0, len(array) - 1, array)

# Performs identical to quick_sort, except returns a new array rather than modifying original
def quick_sort_copy(array: List[T]) -> List[T]:
    new_array: List[T] = array[:]
    perform_quick_sort(0, len(new_array) - 1, new_array)
    return new_array

# Quick sort partition algorithm component for sorting an array
def quick_sort_partition(start: int, end: int, array: List[T]) -> int:
    pivot_index: int = start
    pivot: T = array[pivot_index]
    while start < end:
        # Get next larger than pivot from left
        while start < len(array) and array[start] <= pivot:
            start += 1
        # Get next smaller than pivot from right
        while array[end] > pivot:
            end -= 1
        if start < end:
            array[start], array[end] = array[end], array[start]
    array[end], array[pivot_index] = array[pivot_index], array[end]
    return end

# Sorts parametized array recursively using quick sort algorithm
def perform_quick_sort(start: int, end: int, array: List[T]) -> None:
    if start < end:
        p: int = quick_sort_partition(start, end, array)
        perform_quick_sort(start, p-1, array)
        perform_quick_sort(p+1, end, array)

# Merge sort recursive algorithm for sorting an array 
def merge_sort(array: List[T]) -> None:
    if len(array) > 1:
        mid: int = len(array) // 2
        left_array = array[:mid]
        right_array = array[mid:]
        merge_sort(left_array)
        merge_sort(right_array)
        l: int = 0
        r: int = 0
        i: int = 0
        while l < len(left_array) and r < len(right_array):
            if left_array[l] < right_array[r]:
                array[i] = left_array[l]
                l += 1
            else:
                array[i] = right_array[r]
                r += 1
            i += 1
        while l < len(left_array):
            array[i] = left_array[l]
            l += 1
            i += 1
        while r < len(right_array):
            array[i] = right_array[r]
            r += 1
            i += 1

# Algorithm 1, selects index value after sorting array using merge sort
def select_kth_1(array: List[T], k: int) -> T:
    array_copy: List[T] = array[:]
    merge_sort(array_copy)
    return array_copy[k]

# Algorithm 2, returns k index using partition component of quick sort w/o recurison
def select_kth_2(array: List[T], k: int) -> T:
    # Error handling for invalid k index
    if k >= len(array): 
        return None

    # Initialize start and end indexes
    start_index: int = 0
    end_index: int = len(array) - 1
    
    # Loop returns a value when partition reaches k'th index
    while True:
        start: int = start_index
        end: int = end_index
        pivot_index: int = start
        pivot: T = array[pivot_index]

        while start < end:
            # Get next "larger than pivot" from left
            while start < len(array) and array[start] <= pivot:
                start += 1
            # Get next "smaller than pivot" from right
            while array[end] > pivot:
                end -= 1
            # Swap the values at start and end indexes if appropriate
            if start < end:
                array[start], array[end] = array[end], array[start]

        # Swap the values at end and pivot_index
        array[end], array[pivot_index] = array[pivot_index], array[end]
        if pivot_index == k:
            # Found result
            return array[pivot_index]
        if pivot_index > k:
            # Partition lower array values
            end_index = pivot_index - 1
        else:
            # Partition higher array values
            start_index = pivot_index + 1

# Algorithm 3, returns k index using partition component of quick sort w/ recurison
def perform_select_kth_3(array: List[T], start_index: int, end_index: int, k: int) -> T:
    start: int = start_index
    end: int = end_index
    pivot_index: int = start
    pivot: T = array[pivot_index]
    while start < end:
        while start < len(array) and array[start] <= pivot:
            start += 1
        # Get next smaller than pivot from right
        while array[end] > pivot:
            end -= 1
        if start < end:
            array[start], array[end] = array[end], array[start]
    array[end], array[pivot_index] = array[pivot_index], array[end]
    if pivot_index == k:
        return array[pivot_index]
    if pivot_index > k:
        return perform_select_kth_3(array, start_index, pivot_index - 1, k)
    else:
        return perform_select_kth_3(array, pivot_index + 1, end_index, k)

# Parametizes array for recursive Algorithm 3
def select_kth_3(array: List[T], k: int) -> T:
    if k >= len(array): 
        return None
    return perform_select_kth_3(array[:], 0, len(array) - 1, k)

# Parametizes array for recursive Algorithm 3
def select_kth_4(array: List[T], k: int) -> T:
    if k >= len(array): 
        return None
    return perform_select_kth_4(array[:], 0, len(array) - 1, k)

# Algorithm 4, used median of medians for pivot index to increase efficiency of partition algorithm
def perform_select_kth_4(array: List[T], start_index: int, end_index: int, k: int) -> T:
    start: int = start_index
    end: int = end_index
    pivot_index: int = (start_index + end_index) // 2
    pivot: T = array[pivot_index]
    while start < end:
        while start < len(array) and array[start] <= pivot:
            start += 1
        # Get next smaller than pivot from right
        while array[end] > pivot:
            end -= 1
        if start < end:
            array[start], array[end] = array[end], array[start]
    array[end], array[pivot_index] = array[pivot_index], array[end]
    if pivot_index == k:
        return array[pivot_index]
    if pivot_index > k:
        return perform_select_kth_3(array, start_index, pivot_index - 1, k)
    else:
        return perform_select_kth_3(array, pivot_index + 1, end_index, k)

# Generates an array of ints of specified size 
def generate_size_n_array(n: int) -> List[int]:
    return [random.randint(0, 100000) for _ in range(n)]

# Selects algorithm for calculation by specified i index value
def get_algorithm(i: int, array: List[T], k: int) -> T:
    if i == 1: return select_kth_1(array, i)
    elif i == 2: return select_kth_2(array, k)
    elif i == 3: return select_kth_3(array, k)
    elif i == 4: return select_kth_4(array, k)

# Quantity of iterations to calculate
iterations: int = 10  

# K values that will be used to test algorithm sorted k index value retrieval
k_values: List[float] = [0, .25, .5, .75, 1]

# List of array sizes to be tested 
array_sizes: List[int] = [10, 50, 100, 250, 500, 1000, 2500, 10000]

# Test each algorithm for each size, for each k index selection,
# for specified iterations, to return a average calculation time for each algorithm

for array_size in array_sizes:
    arrays = [generate_size_n_array(array_size) for _ in range(iterations)]
    for i in range(1, 5):
        start: time = time.time()
        for k_value in k_values:
            k = min(math.floor(k_value * array_size), array_size -1)
            for array in arrays:
                get_algorithm(i, array, k)
        end = time.time()
        elapsed: time = end - start
        print(f"Algorithm {i} \t {elapsed} \t avg: {elapsed / (iterations * len(k_values))} \t n={array_size}.")



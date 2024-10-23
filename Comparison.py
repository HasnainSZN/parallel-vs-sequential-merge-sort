import time
import random
from multiprocessing import Pool

# Helper function to merge two arrays
def merge(arr1, arr2):
    result = []
    i = j = 0
    while i < len(arr1) and j < len(arr2):
        if arr1[i] < arr2[j]:
            result.append(arr1[i])
            i += 1
        else:
            result.append(arr2[j])
            j += 1
    result.extend(arr1[i:])
    result.extend(arr2[j:])
    return result

# Sequential merge sort function (with return)
def merge_sort(arr):
    if len(arr) > 1:
        mid = len(arr) // 2
        L = arr[:mid]
        R = arr[mid:]
        L = merge_sort(L)
        R = merge_sort(R)
        arr = merge(L, R)
    return arr

# Parallel merge sort function
def parallel_merge_sort(arr):
    if len(arr) <= 1:
        return arr

    # Set a threshold for parallelism, below which it falls back to sequential
    if len(arr) < 50000:
        return sorted(arr)
    
    mid = len(arr) // 2
    
    # Perform parallel processing only at the top level
    with Pool(2) as pool:
        left, right = pool.map(merge_sort, [arr[:mid], arr[mid:]])
    
    # Merge the two halves
    return merge(left, right)

# Measure execution time of a sorting function
def measure_time(sort_function, arr):
    start = time.time()
    sort_function(arr.copy())
    end = time.time()
    return end - start

# Main block to prevent multiprocessing error on Windows
if __name__ == '__main__':
    import matplotlib.pyplot as plt

    sizes = [10000, 50000, 100000, 500000, 1000000]
    seq_times = []
    par_times = []

    for size in sizes:
        arr = [random.randint(0, 1000000) for _ in range(size)]
        seq_times.append(measure_time(merge_sort, arr))
        par_times.append(measure_time(parallel_merge_sort, arr))

    # Plotting the results
    plt.plot(sizes, seq_times, label='Sequential')
    plt.plot(sizes, par_times, label='Parallel')
    plt.xlabel('Input Size')
    plt.ylabel('Execution Time (seconds)')
    plt.legend()
    plt.show()

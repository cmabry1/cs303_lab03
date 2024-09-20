import random
import time
import matplotlib.pyplot as plt
import pandas as pd

def insertion_sort(A):
    for j in range(1, len(A)):
        key = A[j]
        i = j - 1
        while i >= 0 and A[i] > key:
            A[i + 1] = A[i]
            i -= 1
        A[i + 1] = key

def merge_sort(arr, temp, p, r):
    if p < r:
        q = (p + r) // 2
        merge_sort(arr, temp, p, q)
        merge_sort(arr, temp, q + 1, r)
        merge(arr, temp, p, q, r)

def merge(arr, temp, p, q, r):
    i = p
    j = q + 1
    for k in range(p, r + 1):
        temp[k] = arr[k]
    for k in range(p, r + 1):
        if i > q:
            arr[k] = temp[j]
            j += 1
        elif j > r:
            arr[k] = temp[i]
            i += 1
        elif temp[j] < temp[i]:
            arr[k] = temp[j]
            j += 1
        else:
            arr[k] = temp[i]
            i += 1

def hybrid_merge_sort(arr, temp, p, r, threshold):
    if r - p + 1 <= threshold:
        insertion_sort(arr[p:r + 1])
    else:
        if p < r:
            q = (p + r) // 2
            hybrid_merge_sort(arr, temp, p, q, threshold)
            hybrid_merge_sort(arr, temp, q + 1, r, threshold)
            merge(arr, temp, p, q, r)

def read_arrays_from_file(filename):
    arrays = []
    try:
        with open(filename, 'r') as file:
            for line in file:
                line = line.strip() 
                if line: 
                    cleaned_line = line.replace(',', ' ')
                    try:
                        array = list(map(int, cleaned_line.split()))
                        arrays.append(array)
                    except ValueError as e:
                        print(f"Error reading line '{line}' in file {filename}: {e}")
    except FileNotFoundError:
        print(f"File {filename} not found.")
    except Exception as e:
        print(f"An error occurred: {e}")
    return arrays

def test_merge_sort(arrays):
    merge_times = []
    for arr in arrays:
        temp = [0] * len(arr)
        start_time = time.time_ns()  
        merge_sort(arr, temp, 0, len(arr) - 1)
        end_time = time.time_ns()
        merge_times.append(end_time - start_time)
        print(f"Array size: {len(arr)}, Time taken by Merge Sort: {end_time - start_time} nanoseconds")
    return merge_times

def test_insertion_sort(arrays):
    insertion_times = []

    for arr in arrays:
        start_time = time.time_ns()  
        insertion_sort(arr)
        end_time = time.time_ns()
        insertion_times.append(end_time - start_time)
        print(f"Array size: {len(arr)}, Time taken by Insertion Sort: {end_time - start_time} nanoseconds")
    return insertion_times

def test_hybrid_merge_sort(arrays, thresholds):
    hybrid_times = {t: [] for t in thresholds}
    for threshold in thresholds:
        print(f"\nTesting hybrid merge sort with threshold {threshold}:")
        for arr in arrays:
            temp = [0] * len(arr)
            start_time = time.time_ns()  
            hybrid_merge_sort(arr, temp, 0, len(arr) - 1, threshold)
            end_time = time.time_ns()
            hybrid_times[threshold].append(end_time - start_time)
            print(f"Array size: {len(arr)}, Time taken by Hybrid Merge Sort with threshold {threshold}: {end_time - start_time} nanoseconds")
    return hybrid_times

def plot_results(array_sizes, merge_times, insertion_times, hybrid_times):
    plt.figure(figsize=(12, 8))
    plt.plot(array_sizes, merge_times, label='Merge Sort', marker='o')
    plt.plot(array_sizes, insertion_times, label='Insertion Sort', marker='x')
    for threshold, times in hybrid_times.items():
        plt.plot(array_sizes, times, label=f'Hybrid Merge Sort (threshold={threshold})', marker='^')
    plt.xlabel('Array Size')
    plt.ylabel('Execution Time (nanoseconds)')
    plt.title('Sorting Algorithms: Merge Sort, Insertion Sort, and Hybrid Merge Sort')
    plt.legend()
    plt.grid(True)
    plt.show()

def display_table(array_sizes, merge_times, insertion_times, hybrid_times):
    thresholds = [10, 20, 50, 100]
    data = {
        'Array Size': array_sizes,
        'Merge Sort (ns)': merge_times,
        'Insertion Sort (ns)': insertion_times,
    }
    for threshold in thresholds:
        data[f'Hybrid Merge Sort (threshold={threshold}) (ns)'] = hybrid_times[threshold]
    df = pd.DataFrame(data)
    print(df.to_string(index=False))  
    return df

def test_sorting_algorithms_for_files(filenames, thresholds):
    all_merge_times = []
    all_insertion_times = []
    all_hybrid_times = {t: [] for t in thresholds}
    all_array_sizes = []
    for filename in filenames:
        arrays = read_arrays_from_file(filename)  
        array_sizes = [len(arr) for arr in arrays]
        all_array_sizes.extend(array_sizes)
        print(f"\nProcessing file: {filename}")
        merge_times = test_merge_sort(arrays.copy())
        all_merge_times.extend(merge_times)
        insertion_times = test_insertion_sort(arrays.copy())
        all_insertion_times.extend(insertion_times)
        hybrid_times = test_hybrid_merge_sort(arrays.copy(), thresholds)
        for threshold in thresholds:
            all_hybrid_times[threshold].extend(hybrid_times[threshold])
    plot_results(all_array_sizes, all_merge_times, all_insertion_times, all_hybrid_times)
    table_df = display_table(all_array_sizes, all_merge_times, all_insertion_times, all_hybrid_times)
    return table_df

def print_before_and_after_sort(filename):
    arrays = read_arrays_from_file(filename)  
    print(f"Arrays from {filename} before sorting:")
    for arr in arrays:
        print(arr)
    print(f"\nArrays from {filename} after Merge Sort:")
    for arr in arrays:
        temp = [0] * len(arr)
        merge_sort(arr, temp, 0, len(arr) - 1)
        print(arr)
    arrays = read_arrays_from_file(filename)
    print(f"\nArrays from {filename} after Insertion Sort:")
    for arr in arrays:
        insertion_sort(arr)
        print(arr)


def main():
    filenames = ['1000.txt', '2500.txt', '5000.txt','10000.txt','25000.txt','50000.txt','100000.txt','250000.txt','500000.txt','1000000.txt']  
    thresholds = [10, 20, 50, 100]  
    print_before_and_after_sort('1000.txt')
    results_df = test_sorting_algorithms_for_files(filenames, thresholds)
    print(f"\nCombined Results for all files:")
    print(results_df)

if __name__ == '__main__':
    main()

import random
import time
import matplotlib.pyplot as plt
import pandas as pd

# Insertion Sort Implementation
def insertion_sort(A):
    for j in range(1, len(A)):
        key = A[j]
        i = j - 1
        while i >= 0 and A[i] > key:
            A[i + 1] = A[i]
            i -= 1
        A[i + 1] = key

# Merge Sort Implementation
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

# Hybrid Merge Sort
def hybrid_merge_sort(arr, temp, p, r, threshold):
    if r - p + 1 <= threshold:
        insertion_sort(arr[p:r + 1])
    else:
        if p < r:
            q = (p + r) // 2
            hybrid_merge_sort(arr, temp, p, q, threshold)
            hybrid_merge_sort(arr, temp, q + 1, r, threshold)
            merge(arr, temp, p, q, r)

# Function to read arrays from a single text file
def read_arrays_from_file(filename):
    arrays = []
    with open(filename, 'r') as file:
        for line in file:
            array = list(map(int, line.strip().split()))
            arrays.append(array)
    return arrays

# Function to read arrays from multiple text files
def read_arrays_from_multiple_files(filenames):
    all_arrays = []
    for filename in filenames:
        arrays = read_arrays_from_file(filename)
        all_arrays.extend(arrays)  # Add arrays from this file to the overall list
    return all_arrays

# Test Merge Sort and record time in nanoseconds
def test_merge_sort(arrays):
    merge_times = []

    for arr in arrays:
        temp = [0] * len(arr)
        start_time = time.time_ns()  # Measure time in nanoseconds
        merge_sort(arr, temp, 0, len(arr) - 1)
        end_time = time.time_ns()
        merge_times.append(end_time - start_time)
        print(f"Array size: {len(arr)}, Time taken by Merge Sort: {end_time - start_time} nanoseconds")

    return merge_times

# Test Insertion Sort and record time in nanoseconds
def test_insertion_sort(arrays):
    insertion_times = []

    for arr in arrays:
        start_time = time.time_ns()  # Measure time in nanoseconds
        insertion_sort(arr)
        end_time = time.time_ns()
        insertion_times.append(end_time - start_time)
        print(f"Array size: {len(arr)}, Time taken by Insertion Sort: {end_time - start_time} nanoseconds")

    return insertion_times

# Test Hybrid Merge Sort and record time in nanoseconds
def test_hybrid_merge_sort(arrays, thresholds):
    hybrid_times = {t: [] for t in thresholds}

    for threshold in thresholds:
        print(f"\nTesting hybrid merge sort with threshold {threshold}:")
        for arr in arrays:
            temp = [0] * len(arr)
            start_time = time.time_ns()  # Measure time in nanoseconds
            hybrid_merge_sort(arr, temp, 0, len(arr) - 1, threshold)
            end_time = time.time_ns()
            hybrid_times[threshold].append(end_time - start_time)
            print(f"Array size: {len(arr)}, Time taken by Hybrid Merge Sort with threshold {threshold}: {end_time - start_time} nanoseconds")

    return hybrid_times

# Plotting function to visualize the results
def plot_results(array_sizes, merge_times, insertion_times, hybrid_times):
    # Plot Merge Sort vs Insertion Sort
    plt.plot(array_sizes, merge_times, label='Merge Sort')
    plt.plot(array_sizes, insertion_times, label='Insertion Sort')
    
    for threshold, times in hybrid_times.items():
        plt.plot(array_sizes, times, label=f'Hybrid Merge Sort (threshold={threshold})')

    plt.xlabel('Array Size')
    plt.ylabel('Execution Time (nanoseconds)')
    plt.title('Sorting Algorithms: Merge Sort, Insertion Sort, and Hybrid Merge Sort')
    plt.legend()
    plt.show()

# Function to create and display a table of results
def display_table(array_sizes, merge_times, insertion_times, hybrid_times):
    thresholds = [10, 20, 50, 100]

    # Create a DataFrame to store the results
    data = {
        'Array Size': array_sizes,
        'Merge Sort (ns)': merge_times,
        'Insertion Sort (ns)': insertion_times,
    }

    for threshold in thresholds:
        data[f'Hybrid Merge Sort (threshold={threshold}) (ns)'] = hybrid_times[threshold]

    df = pd.DataFrame(data)
    
    # Display the table
    print(df.to_string(index=False))  # Print the table without the index
    return df

# Run and collect timing data
def main():
    filenames = ['1000.txt', '2500.txt', '5000.txt','10000.txt','25000.txt','50000.txt','100000.txt','250000.txt','500000.txt','1000000.txt']  # List of text files
    arrays = read_arrays_from_multiple_files(filenames)  # Read arrays from multiple files
    array_sizes = [len(arr) for arr in arrays]

    merge_times = test_merge_sort(arrays.copy())
    insertion_times = test_insertion_sort(arrays.copy())
    hybrid_times = test_hybrid_merge_sort(arrays.copy(), thresholds=[10, 20, 50, 100])

    # Plot the results
    plot_results(array_sizes, merge_times, insertion_times, hybrid_times)

    # Display the table
    table_df = display_table(array_sizes, merge_times, insertion_times, hybrid_times)

if __name__ == '__main__':
    main()

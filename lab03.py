import random
import time
import matplotlib.pyplot as plt
import pandas as pd
import sys

# Set the maximum number of digits for integers
sys.set_int_max_str_digits(10000000)

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

# Hybrid Merge Sort Implementation
def hybrid_merge_sort(arr, temp, p, r, threshold):
    if r - p + 1 <= threshold:
        insertion_sort(arr[p:r + 1])
    else:
        if p < r:
            q = (p + r) // 2
            hybrid_merge_sort(arr, temp, p, q, threshold)
            hybrid_merge_sort(arr, temp, q + 1, r, threshold)
            merge(arr, temp, p, q, r)

# Function to read arrays from a single text file and handle commas
def read_arrays_from_file(filename):
    arrays = []
    try:
        with open(filename, 'r') as file:
            for line in file:
                line = line.strip()  # Remove leading/trailing whitespaces
                if line:  # Ensure the line isn't empty
                    # Replace commas with spaces, then split and convert to integers
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
    plt.figure(figsize=(12, 8))

    # Plot Merge Sort vs Insertion Sort
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

# Function to test sorting algorithms for each file separately and combine the results
def test_sorting_algorithms_for_files(filenames, thresholds):
    all_merge_times = []
    all_insertion_times = []
    all_hybrid_times = {t: [] for t in thresholds}
    all_array_sizes = []

    for filename in filenames:
        arrays = read_arrays_from_file(filename)  # Read arrays from the file
        array_sizes = [len(arr) for arr in arrays]
        all_array_sizes.extend(array_sizes)
        
        print(f"\nProcessing file: {filename}")
        
        # Test Merge Sort and record time in nanoseconds
        merge_times = test_merge_sort(arrays.copy())
        all_merge_times.extend(merge_times)
        
        # Test Insertion Sort and record time in nanoseconds
        insertion_times = test_insertion_sort(arrays.copy())
        all_insertion_times.extend(insertion_times)
        
        # Test Hybrid Merge Sort and record time in nanoseconds
        hybrid_times = test_hybrid_merge_sort(arrays.copy(), thresholds)
        for threshold in thresholds:
            all_hybrid_times[threshold].extend(hybrid_times[threshold])
    
    # Plot the results for all files
    plot_results(all_array_sizes, all_merge_times, all_insertion_times, all_hybrid_times)
    
    # Display the table
    table_df = display_table(all_array_sizes, all_merge_times, all_insertion_times, all_hybrid_times)
    return table_df

# Main function
def main():
    filenames = ['1000.txt', '2500.txt', '5000.txt','10000.txt','25000.txt','50000.txt','100000.txt','250000.txt','500000.txt','1000000.txt']  # List of text files
    thresholds = [10, 20, 50, 100]  # Different thresholds for hybrid merge sort

    # Test sorting algorithms for all files and collect results
    results_df = test_sorting_algorithms_for_files(filenames, thresholds)

    # Optionally, print or save the results
    print(f"\nCombined Results for all files:")
    print(results_df)

if __name__ == '__main__':
    main()

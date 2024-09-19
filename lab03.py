import random
import time
import matplotlib.pyplot as plt
import pandas as pd  # For creating and displaying the table

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

# Helper function to generate random arrays
def generate_array(n):
    return [random.randint(1, 10000) for _ in range(n)]

# Test Merge Sort and record time in nanoseconds
def test_merge_sort():
    array_lengths = [100, 1000, 5000, 10000]
    merge_times = []

    for n in array_lengths:
        arr = generate_array(n)
        temp = [0] * n
        start_time = time.time_ns()  # Measure time in nanoseconds
        merge_sort(arr, temp, 0, n - 1)
        end_time = time.time_ns()
        merge_times.append(end_time - start_time)
        print(f"Array size: {n}, Time taken by Merge Sort: {end_time - start_time} nanoseconds")

    return merge_times

# Test Insertion Sort and record time in nanoseconds
def test_insertion_sort():
    array_lengths = [100, 1000, 5000, 10000]
    insertion_times = []

    for n in array_lengths:
        arr = generate_array(n)
        start_time = time.time_ns()  # Measure time in nanoseconds
        insertion_sort(arr)
        end_time = time.time_ns()
        insertion_times.append(end_time - start_time)
        print(f"Array size: {n}, Time taken by Insertion Sort: {end_time - start_time} nanoseconds")

    return insertion_times

# Test Hybrid Merge Sort and record time in nanoseconds
def test_hybrid_merge_sort():
    array_lengths = [100, 1000, 5000, 10000]
    thresholds = [10, 20, 50, 100]  # Different cutoff values
    hybrid_times = {t: [] for t in thresholds}

    for threshold in thresholds:
        print(f"\nTesting hybrid merge sort with threshold {threshold}:")
        for n in array_lengths:
            arr = generate_array(n)
            temp = [0] * n
            start_time = time.time_ns()  # Measure time in nanoseconds
            hybrid_merge_sort(arr, temp, 0, n - 1, threshold)
            end_time = time.time_ns()
            hybrid_times[threshold].append(end_time - start_time)
            print(f"Array size: {n}, Time taken by Hybrid Merge Sort with threshold {threshold}: {end_time - start_time} nanoseconds")

    return hybrid_times

# Plotting function to visualize the results
def plot_results(merge_times, insertion_times, hybrid_times):
    array_lengths = [100, 1000, 5000, 10000]

    # Plot Merge Sort vs Insertion Sort
    plt.plot(array_lengths, merge_times, label='Merge Sort')
    plt.plot(array_lengths, insertion_times, label='Insertion Sort')
    
    for threshold, times in hybrid_times.items():
        plt.plot(array_lengths, times, label=f'Hybrid Merge Sort (threshold={threshold})')

    plt.xlabel('Array Size')
    plt.ylabel('Execution Time (nanoseconds)')
    plt.title('Sorting Algorithms: Merge Sort, Insertion Sort, and Hybrid Merge Sort')
    plt.legend()
    plt.show()

# Function to create and display a table of results
def display_table(merge_times, insertion_times, hybrid_times):
    array_lengths = [100, 1000, 5000, 10000]
    thresholds = [10, 20, 50, 100]

    # Create a DataFrame to store the results
    data = {
        'Array Size': array_lengths,
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
merge_times = test_merge_sort()
insertion_times = test_insertion_sort()
hybrid_times = test_hybrid_merge_sort()

# Plot the results
plot_results(merge_times, insertion_times, hybrid_times)

# Display the table
table_df = display_table(merge_times, insertion_times, hybrid_times)

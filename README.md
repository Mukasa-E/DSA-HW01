# DSA-HW01
# Data-structures-Algorithms


# UniqueInt Processor

This program is designed to process input files containing integer data and produce corresponding output files. It measures the runtime and memory usage for each file processed.

## Features

- Processes multiple input files concurrently
- Measures runtime and memory usage for each file processed
- Supports customizable input and output file paths

## Requirements

- Python 3.x
- tracemalloc module (for memory usage measurement)

## Usage

1. Clone the repository to your local machine.
2. Navigate to the project directory.
3. Ensure you have Python 3.x installed.
4. Install the tracemalloc module if you haven't already:
    ```
    pip install tracemalloc
    ```
5. Run the UniqueInt.py script:
    ```
    python3 UniqueInt.py
    ```
6. The program will process the input files specified in the script and generate corresponding output files. It will print the runtime and memory usage for each file processed.

## Customization

You can customize the input and output file paths by modifying the `input_file_paths` and `output_file_paths` lists in the `if __name__ == "__main__":` block of the UniqueInt.py script.

## Example

```python
if __name__ == "__main__":
    unique_int_processor = UniqueInt()
    input_file_paths = [
        "sample_inputs/small_sample_input_01.txt",
        "sample_inputs/small_sample_input_02.txt",
        "sample_inputs/small_sample_input_03.txt",
        "sample_inputs/small_sample_input_04.txt"
        # Add more file paths as needed
    ]

    output_file_paths = [
        "sample_results/small_sample_results_01.txt",
        "sample_results/small_sample_results_02.txt",
        "sample_results/small_sample_results_03.txt",
        "sample_results/small_sample_results_04.txt",
        # Add corresponding output file paths
    ]
    unique_int_processor.processFiles(input_file_paths, output_file_paths)
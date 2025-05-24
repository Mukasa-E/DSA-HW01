import os

class SparseMatrix:
    def __init__(self, matrixFilePath=None, numRows=0, numCols=0):
        self.rows = numRows
        self.cols = numCols
        self.matrix_data = {}

        if matrixFilePath:
            self._load_from_file(matrixFilePath)
        elif numRows <= 0 or numCols <= 0:
            raise ValueError("For an empty matrix, numRows and numCols must be positive.")

    def _load_from_file(self, matrixFilePath):
        if not os.path.exists(matrixFilePath):
            raise FileNotFoundError(f"Matrix file not found at: {matrixFilePath}")

        with open(matrixFilePath, 'r') as f:
            lines = f.readlines()

        try:
            rows_str = lines[0].strip()
            cols_str = lines[1].strip()

            if not rows_str.startswith("rows=") or not cols_str.startswith("cols="):
                raise ValueError

            self.rows = int(rows_str[len("rows="):])
            self.cols = int(cols_str[len("cols="):])

            if self.rows <= 0 or self.cols <= 0:
                raise ValueError("Matrix dimensions must be positive.")

        except (IndexError, ValueError):
            raise ValueError("Input file has wrong format: Missing or invalid rows/cols definitions.")

        for i in range(2, len(lines)):
            line = lines[i].strip()
            if not line:
                continue

            if not (line.startswith('(') and line.endswith(')')):
                raise ValueError("Input file has wrong format: Entry not enclosed in parentheses.")

            content = line[1:-1]

            parts = content.split(',')
            if len(parts) != 3:
                raise ValueError("Input file has wrong format: Entry does not have 3 comma-separated values.")

            try:
                row = int(parts[0].strip())
                col = int(parts[1].strip())
                value = int(parts[2].strip())
            except ValueError:
                raise ValueError("Input file has wrong format: Row, column, or value is not an integer.")

            if not (0 <= row < self.rows and 0 <= col < self.cols):
                raise ValueError(f"Input file has wrong format: Entry ({row}, {col}) out of bounds for matrix "
                                 f"dimensions ({self.rows}, {self.cols}).")

            if value != 0:
                self.matrix_data[(row, col)] = value

    def getElement(self, currRow, currCol):
        if not (0 <= currRow < self.rows and 0 <= currCol < self.cols):
            raise IndexError(f"({currRow}, {currCol}) is out of bounds for matrix of size ({self.rows}, {self.cols})")
        return self.matrix_data.get((currRow, currCol), 0)

    def setElement(self, currRow, currCol, value):
        if not (0 <= currRow < self.rows and 0 <= currCol < self.cols):
            raise IndexError(f"({currRow}, {currCol}) is out of bounds for matrix of size ({self.rows}, {self.cols})")

        if value != 0:
            self.matrix_data[(currRow, currCol)] = value
        elif (currRow, currCol) in self.matrix_data:
            del self.matrix_data[(currRow, currCol)]

    def add(self, other_matrix):
        if self.rows != other_matrix.rows or self.cols != other_matrix.cols:
            raise ValueError("Matrix dimensions must match for addition.")

        result_matrix = SparseMatrix(numRows=self.rows, numCols=self.cols)

        for (r, c), val in self.matrix_data.items():
            result_matrix.setElement(r, c, val)

        for (r, c), val in other_matrix.matrix_data.items():
            current_val = result_matrix.getElement(r, c)
            result_matrix.setElement(r, c, current_val + val)

        return result_matrix

    def subtract(self, other_matrix):
        if self.rows != other_matrix.rows or self.cols != other_matrix.cols:
            raise ValueError("Matrix dimensions must match for subtraction.")

        result_matrix = SparseMatrix(numRows=self.rows, numCols=self.cols)

        for (r, c), val in self.matrix_data.items():
            result_matrix.setElement(r, c, val)

        for (r, c), val in other_matrix.matrix_data.items():
            current_val = result_matrix.getElement(r, c)
            result_matrix.setElement(r, c, current_val - val)

        return result_matrix

    def multiply(self, other_matrix):
        if self.cols != other_matrix.rows:
            raise ValueError("Number of columns in the first matrix must equal "
                             "number of rows in the second matrix for multiplication.")

        result_matrix = SparseMatrix(numRows=self.rows, numCols=other_matrix.cols)

        for (r1, c1), val1 in self.matrix_data.items():
            for (r2, c2), val2 in other_matrix.matrix_data.items():
                if c1 == r2:
                    current_sum = result_matrix.getElement(r1, c2)
                    result_matrix.setElement(r1, c2, current_sum + (val1 * val2))
        return result_matrix

    def to_string(self):
        output = f"rows={self.rows}\ncols={self.cols}\n"
        sorted_keys = sorted(self.matrix_data.keys())
        for r, c in sorted_keys:
            output += f"({r}, {c}, {self.matrix_data[(r, c)]})\n"
        return output

def main():
    print("Welcome to the Sparse Matrix Operations Program!")
    print("Please ensure your input files are located in: /dsa/sparse_matrix/sample_inputs/")

    while True:
        print("\n--- Choose a Matrix Operation ---")
        print("1. Addition")
        print("2. Subtraction")
        print("3. Multiplication")
        print("4. Exit")

        choice = input("Enter your choice (1-4): ")

        if choice == '4':
            print("Exiting program. Happy coding!")
            break

        if choice not in ['1', '2', '3']:
            print("Invalid choice. Please enter a number between 1 and 4.")
            continue

        file1_path = input("Enter path for the first matrix file (e.g., matrix1.txt): ")
        file2_path = input("Enter path for the second matrix file (e.g., matrix2.txt): ")

        base_input_path = os.path.join("dsa", "sparse_matrix", "sample_inputs")
        full_file1_path = os.path.join(base_input_path, file1_path)
        full_file2_path = os.path.join(base_input_path, file2_path)

        matrix1 = None
        matrix2 = None

        try:
            print(f"Loading matrix 1 from: {full_file1_path}")
            matrix1 = SparseMatrix(matrixFilePath=full_file1_path)
            print(f"Loading matrix 2 from: {full_file2_path}")
            matrix2 = SparseMatrix(matrixFilePath=full_file2_path)
        except (FileNotFoundError, ValueError) as e:
            print(f"Error loading matrices: {e}")
            continue

        result_matrix = None
        operation_name = ""

        try:
            if choice == '1':
                operation_name = "Addition"
                result_matrix = matrix1.add(matrix2)
            elif choice == '2':
                operation_name = "Subtraction"
                result_matrix = matrix1.subtract(matrix2)
            elif choice == '3':
                operation_name = "Multiplication"
                result_matrix = matrix1.multiply(matrix2)

            print(f"\n--- Result of {operation_name} ---")
            print(result_matrix.to_string())

            output_filename = f"result_{operation_name.lower()}_{os.path.basename(file1_path).split('.')[0]}_" \
                              f"{os.path.basename(file2_path).split('.')[0]}.txt"
            output_dir = os.path.join("dsa", "sparse_matrix", "output")
            os.makedirs(output_dir, exist_ok=True)
            output_filepath = os.path.join(output_dir, output_filename)

            with open(output_filepath, 'w') as f:
                f.write(result_matrix.to_string())
            print(f"Result saved to: {output_filepath}")

        except ValueError as e:
            print(f"Error during matrix operation: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
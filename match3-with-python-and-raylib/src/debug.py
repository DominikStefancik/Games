def print_matrix(matrix):
    for row in range(len(matrix)):
        print(matrix[row])


def print_mapped_matrix(matrix, map_function):
    for row in range(len(matrix)):
        mapped_row = list(map(map_function, matrix[row]))
        print(mapped_row)

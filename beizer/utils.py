# -*- coding: utf-8 -*-


def matrix_is_quadratic(matrix):
    """Returns True if matrix is quadratic."""
    len_matrix = len(matrix)
    return all(len_matrix == len(row) for row in matrix)

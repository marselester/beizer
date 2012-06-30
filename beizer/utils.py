# -*- coding: utf-8 -*-


def matrix_is_quadratic(matrix):
    """Returns True if matrix is quadratic."""
    try:
        len_matrix = len(matrix)
        quadratic = all(len_matrix == len(row) for row in matrix)
    except TypeError:
        quadratic = False
    finally:
        return quadratic

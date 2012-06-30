# -*- coding: utf-8 -*-
import unittest

from beizer.models import TransitionMatrix
from beizer.exceptions import MatrixInitError


class MatrixInitTest(unittest.TestCase):
    def test_init_takes_at_least_two_arguments(self):
        self.assertRaises(TypeError, TransitionMatrix)

    def test_argument_is_not_list(self):
        matrix = 'some wrong value'
        self.assertRaises(MatrixInitError, TransitionMatrix, (matrix))

    def test_empty_list(self):
        matrix = []

    def test_matrix_is_not_quadratic(self):
        matrix = [
            [(0.6, 10), None],
            [None]
        ]

    def test_matrix_has_only_source(self):
        matrix = [
            [None]
        ]
        self.assertEqual(TransitionMatrix(matrix), '[[None]]')

if __name__ == '__main__':
    unittest.main()

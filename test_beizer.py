# -*- coding: utf-8 -*-
import unittest

from beizer.models import TransitionMatrix, Transition, _exclude_trans
from beizer.exceptions import MatrixInitError, LoopExcludeError


class MatrixInitTest(unittest.TestCase):

    def test_init_takes_at_least_two_arguments(self):
        self.assertRaises(TypeError, TransitionMatrix)

    def test_argument_is_not_list(self):
        matrix = 'some wrong value'
        self.assertRaises(MatrixInitError, TransitionMatrix, (matrix))

    def test_empty_list(self):
        matrix = []
        self.assertEqual(repr(TransitionMatrix(matrix)), '[]')

    def test_matrix_is_not_quadratic(self):
        matrix = [
            [(0.6, 10), None],
            [None]
        ]
        self.assertRaises(MatrixInitError, TransitionMatrix, (matrix))

    def test_matrix_has_only_source(self):
        matrix = [
            [None]
        ]
        self.assertEqual(repr(TransitionMatrix(matrix)), '[[None]]')


class ExcludeFirstLoopTest(unittest.TestCase):

    def test_matrix_2x2_has_not_got_loop(self):
        matrix = [
            [None, (0.4, 7)],
            [None, None]
        ]
        trans_matrix = TransitionMatrix(matrix)
        self.assertRaises(LoopExcludeError, trans_matrix.exclude_first_loop)

    def test_matrix_2x2_source_has_loop(self):
        matrix = [
            [(0.6, 10), (0.4, 7)],
            [None, None]
        ]
        trans_matrix = TransitionMatrix(matrix)
        trans_matrix.exclude_first_loop()
        # probability is 1.0 = 0.4 / (1 - 0.6)
        # expectation is 22.0 = 7 + ((10 * 0.6) / (1 - 0.6))
        self.assertEqual(repr(trans_matrix),
                         '[[None, (P=1.0, E=22.0)], [None, None]]')


class ExlcudeLastVertexTest(unittest.TestCase):

    def test_matrix_4x4_without_loops(self):
        _ = None
        a = Transition(0.4, 7)
        b = Transition(0.6, 10)
        d = Transition(0.5, 7)
        f = Transition(0.5, 10)
        e = Transition(0.7, 10)
        z = Transition(0.3, 7)

        trans_matrix = TransitionMatrix([
            [_, _, b, a],
            [_, _, _, _],
            [_, f, _, d],
            [_, e, z, _]
        ])

        cell_1_2 = _exclude_trans(column_trans=a, row_trans=e, host_cell=_)
        cell_1_3 = _exclude_trans(column_trans=a, row_trans=z, host_cell=b)
        cell_3_2 = _exclude_trans(column_trans=d, row_trans=e, host_cell=f)
        cell_3_3 = _exclude_trans(column_trans=d, row_trans=z, host_cell=_)
        trans_matrix_after_excluding = TransitionMatrix([
            [_, cell_1_2, cell_1_3],
            [_, _, _],
            [_, cell_3_2, cell_3_3],
        ])

        trans_matrix.exclude_last_vertex()
        self.assertEqual(repr(trans_matrix),
                         repr(trans_matrix_after_excluding))

if __name__ == '__main__':
    unittest.main()

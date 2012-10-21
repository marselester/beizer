# -*- coding: utf-8 -*-
import unittest
from decimal import Decimal as D

from beizer.models import (TransitionMatrix, Transition,
                           transform_trans_while_excluding_vertex,
                           transform_trans_while_excluding_loop)
from beizer.exceptions import MatrixInitError, LoopExcludeError

_ = None


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
        a = (0.6, 10)
        matrix = [
            [a, _],
            [_]
        ]
        self.assertRaises(MatrixInitError, TransitionMatrix, (matrix))

    def test_matrix_has_only_source(self):
        matrix = [
            [_]
        ]
        self.assertEqual(repr(TransitionMatrix(matrix)), '[[None]]')


class ExcludeFirstLoopTest(unittest.TestCase):

    def test_matrix_2x2_has_not_got_loop(self):
        a = (0.4, 7)
        matrix = [
            [_, a],
            [_, _]
        ]
        trans_matrix = TransitionMatrix(matrix)
        self.assertRaises(LoopExcludeError, trans_matrix.exclude_first_loop)

    def test_matrix_2x2_source_has_loop(self):
        a = (D('0.6'), 10)
        b = (D('0.4'), 7)
        matrix = [
            [a, b],
            [_, _]
        ]
        trans_matrix = TransitionMatrix(matrix)
        trans_matrix.exclude_first_loop()
        # Probability is 1.0 = 0.4 / (1 - 0.6)
        # Expectation is 22.0 = 7 + ((10 * 0.6) / (1 - 0.6))
        self.assertEqual(repr(trans_matrix),
                         '[[None, (P=1, E=22)], [None, None]]')

    def test_matrix_structure_after_horizontal_transitions_excluding(self):
        b = Transition(D('0.4'), D('10'))
        a = Transition(D('0.6'), D('20'))

        f = Transition(D('0.4'), D('10'))
        g = Transition(D('0.2'), D('5'))
        d = Transition(D('0.4'), D('15'))

        e = Transition(D('0.8'), D('5'))
        z = Transition(D('0.2'), D('10'))

        trans_matrix = TransitionMatrix([
            [_, _, b, a],
            [_, _, _, _],
            [_, f, g, d],
            [_, e, z, _],
        ])

        cell_3_2 = transform_trans_while_excluding_loop(transition=f, loop=g)
        cell_3_4 = transform_trans_while_excluding_loop(transition=d, loop=g)
        trans_matrix_after_excluding = TransitionMatrix([
            [_, _, b, a],
            [_, _, _, _],
            [_, cell_3_2, _, cell_3_4],
            [_, e, z, _],
        ])

        trans_matrix.exclude_first_loop()
        self.assertEqual(repr(trans_matrix),
                         repr(trans_matrix_after_excluding))

    def test_values_after_horizontal_transitions_excluding(self):
        b = Transition(D('0.4'), D('10'))
        a = Transition(D('0.6'), D('20'))

        f = Transition(D('0.4'), D('10'))
        g = Transition(D('0.2'), D('5'))
        d = Transition(D('0.4'), D('15'))

        e = Transition(D('0.8'), D('5'))
        z = Transition(D('0.2'), D('10'))

        trans_matrix = TransitionMatrix([
            [_, _, b, a],
            [_, _, _, _],
            [_, f, g, d],
            [_, e, z, _],
        ])
        trans_matrix.exclude_first_loop()

        # Probability is f.P / (1 - g.P) = 0.4 / (1 - 0.2) = 0.5
        # Expectation is f.E + (g.E * g.P) / (1 - g.P)
        # 10 + (5 * 0.2) / 0.8 = 11.25
        cell_3_2 = Transition(D('0.5'), D('11.25'))
        self.assertEqual(trans_matrix._matrix[2][1], cell_3_2)

        # Probability is d / (1 - g) = 0.4 / (1 - 0.2) = 0.5
        # Expectation is d.E + (g.E * g.P) / (1 - g.P)
        # 15 + (5 * 0.2) / 0.8 = 16.25
        cell_3_4 = Transition(D('0.5'), D('16.25'))
        self.assertEqual(trans_matrix._matrix[2][3], cell_3_4)

    def test_matrix_structure_after_vertical_transitions_excluding(self):
        pass


class ExlcudeLastVertexTest(unittest.TestCase):

    def test_matrix_4x4_without_loops(self):
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

        cell_1_2 = transform_trans_while_excluding_vertex(
            column_trans=a, row_trans=e, host_cell=_)
        cell_1_3 = transform_trans_while_excluding_vertex(
            column_trans=a, row_trans=z, host_cell=b)
        cell_3_2 = transform_trans_while_excluding_vertex(
            column_trans=d, row_trans=e, host_cell=f)
        cell_3_3 = transform_trans_while_excluding_vertex(
            column_trans=d, row_trans=z, host_cell=_)
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

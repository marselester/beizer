# -*- coding: utf-8 -*-
import unittest
from decimal import Decimal as D

from beizer.models import (TransitionMatrix, Transition,
                           transform_trans_while_excluding_vertex,
                           transform_trans_while_excluding_loop,
                           check_sum_of_probabilities)
from beizer.exceptions import MatrixInitError, LoopExcludeError
from beizer.core import reduce_matrix_size

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

    def test_sum_of_probabilities_is_not_equal_to_one(self):
        a = (D('0.6'), 10)
        b = (D('0.39'), 7)
        matrix = [
            [a, b],
            [_, _]
        ]
        self.assertRaises(MatrixInitError, TransitionMatrix, (matrix))


class ExcludeFirstLoopTest(unittest.TestCase):

    def test_matrix_2x2_has_not_got_loop(self):
        a = (1, 7)
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
        # Resource is 22.0 = 7 + ((10 * 0.6) / (1 - 0.6))
        self.assertEqual(repr(trans_matrix),
                         '[[None, (P=1, R=22)], [None, None]]')

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
        # Resource is f.R + (g.R * g.P) / (1 - g.P)
        # 10 + (5 * 0.2) / 0.8 = 11.25
        cell_3_2 = Transition(D('0.5'), D('11.25'))
        self.assertEqual(trans_matrix._matrix[2][1], cell_3_2)

        # Probability is d / (1 - g) = 0.4 / (1 - 0.2) = 0.5
        # Resource is d.R + (g.R * g.P) / (1 - g.P)
        # 15 + (5 * 0.2) / 0.8 = 16.25
        cell_3_4 = Transition(D('0.5'), D('16.25'))
        self.assertEqual(trans_matrix._matrix[2][3], cell_3_4)

    def test_matrix_structure_after_vertical_transitions_excluding(self):
        pass

    def test_values_after_vertical_transitions_excluding(self):
        pass


    def test_sum_of_probabilities_is_equal_to_one_or_zero(self):
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

        all_rows_are_ok_after_excluding_first_loop = all(
            check_sum_of_probabilities(row) for row in trans_matrix._matrix
        )
        self.assertTrue(all_rows_are_ok_after_excluding_first_loop)


class ExlcudeLastVertexTest(unittest.TestCase):

    def test_matrix_structure_without_loops(self):
        b = Transition(D('0.4'), D('10'))
        a = Transition(D('0.6'), D('20'))

        f = Transition(D('0.5'), D('10'))
        d = Transition(D('0.5'), D('15'))

        e = Transition(D('0.8'), D('5'))
        z = Transition(D('0.2'), D('10'))

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

    def test_sum_of_probabilities_is_equal_to_one_or_zero(self):
        b = Transition(D('0.4'), D('10'))
        a = Transition(D('0.6'), D('20'))

        f = Transition(D('0.5'), D('10'))
        d = Transition(D('0.5'), D('15'))

        e = Transition(D('0.8'), D('5'))
        z = Transition(D('0.2'), D('10'))

        trans_matrix = TransitionMatrix([
            [_, _, b, a],
            [_, _, _, _],
            [_, f, _, d],
            [_, e, z, _]
        ])
        trans_matrix.exclude_last_vertex()

        all_rows_are_ok_after_excluding_first_loop = all(
            check_sum_of_probabilities(row) for row in trans_matrix._matrix
        )
        self.assertTrue(all_rows_are_ok_after_excluding_first_loop)


class TransformTransitionWhileExcludingVertexTest(unittest.TestCase):

    def test_host_cell_is_empty(self):
        column_trans = Transition(D('0.6'), D('20'))
        row_trans = Transition(D('0.8'), D('5'))
        # Probability is c.P * r.P = 0.6 * 0.8 = 0.48
        # Resource is c.R + r.R = 25
        expected_intersection = Transition(D('0.48'), D('25'))

        intersection = transform_trans_while_excluding_vertex(
            column_trans, row_trans)
        self.assertEqual(intersection, expected_intersection)

    def test_host_cell_has_value(self):
        column_trans = Transition(D('0.6'), D('8'))
        row_trans = Transition(D('0.2'), D('2'))
        host_cell = Transition(D('0.4'), D('10'))
        # Probability is h.P + (c.P * r.P) = 0.4 + (0.6 * 0.2) = 0.52
        # Resource is (h.P * h.R + c.P * r.P * (c.R + r.R))
        #                / (h.P + c.P * r.P)
        # (0.4 * 10 + 0.6 * 0.2 * (8 + 2)) / 0.52 = 10
        expected_intersection = Transition(D('0.52'), D('10'))

        intersection = transform_trans_while_excluding_vertex(
            column_trans, row_trans, host_cell)
        self.assertEqual(intersection, expected_intersection)


class ReduceMatrixSizeTest(unittest.TestCase):

    def test_matrix_has_one_loop_and_four_vertices(self):
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
        reduce_matrix_size(trans_matrix)

        self.assertTrue(trans_matrix.has_only_source_and_drain())

        trans_from_source_to_drain = trans_matrix._matrix[0][1]
        self.assertEqual(trans_from_source_to_drain.probability, D('1'))

        all_rows_are_ok_after_excluding_first_loop = all(
            check_sum_of_probabilities(row) for row in trans_matrix._matrix
        )
        self.assertTrue(all_rows_are_ok_after_excluding_first_loop)

    def test_matrix_has_four_loops_and_five_vertices(self):
        a = Transition(D('0.15'), D('56'))
        b = Transition(D('0.85'), D('112'))

        c = Transition(D('0.05'), D('8'))
        d = Transition(D('0.95'), D('16'))

        e = Transition(D('0.05'), D('24'))
        f = Transition(D('0.95'), D('48'))

        g = Transition(D('0.90'), D('40'))
        z = Transition(D('0.10'), D('20'))

        trans_matrix = TransitionMatrix([
            [a, _, b, _, _],
            [_, _, _, _, _],
            [_, _, c, d, _],
            [_, _, _, e, f],
            [_, g, _, _, z],
        ])
        reduce_matrix_size(trans_matrix)

        self.assertTrue(trans_matrix.has_only_source_and_drain())

        trans_from_source_to_drain = trans_matrix._matrix[0][1]
        self.assertEqual(trans_from_source_to_drain.probability, D('1'))

        all_rows_are_ok_after_excluding_first_loop = all(
            check_sum_of_probabilities(row) for row in trans_matrix._matrix
        )
        self.assertTrue(all_rows_are_ok_after_excluding_first_loop)

if __name__ == '__main__':
    unittest.main()

# -*- coding: utf-8 -*-
import unittest

from beizer.models import TransitionMatrix


class MatrixInitTest(unittest.TestCase):
    def test_init_takes_at_least_two_arguments(self):
        self.assertRaises(TypeError, TransitionMatrix)

    def test_argument_is_not_list(self):
        pass

    def test_empty_list(self):
        pass

    def test_matrix_is_not_quadratic(self):
        pass

    def test_matrix_has_only_source(self):
        pass

    def test_matrix_has_only_source_and_drain(self):
        pass

    def test_matrix_has_source_and_drain_and_loop(self):
        pass

    def test_matrix_has_one_loop_and_seven_transitions(self):
        pass

if __name__ == '__main__':
    unittest.main()

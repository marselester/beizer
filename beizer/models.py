# -*- coding: utf-8 -*-
from .exceptions import MatrixInitError, LoopExcludeError
from .utils import (matrix_is_quadratic, last_column_of_matrix,
                    last_row_of_matrix)


class Transition(object):
    """Transition with probability in which system spend or allocate resource.
    """

    def __init__(self, probability=0.0, expectation=None):
        """Initializes transition.

        Keyword arguments:
        probability -- probability of transition to vertex (default 0.0)
        expectation -- expected value of resource which spend or allocate in
        transition to vertex (default None)

        """
        self.probability = probability
        self.expectation = expectation

    def __repr__(self):
        return "(P={0}, E={1})".format(self.probability, self.expectation)

    def __getitem__(self, key):
        if key == 0:
            return self.probability
        elif key == 1:
            return self.expectation
        else:
            raise IndexError('key has to be 0 for probability'
                             ' or 1 for expectation')


class TransitionMatrix(object):
    """Transition matrix."""

    def __init__(self, src_matrix):
        """Initializes transition matrix."""
        if not isinstance(src_matrix, list):
            raise MatrixInitError('expected a list object')
        if not matrix_is_quadratic(src_matrix):
            raise MatrixInitError('matrix has to be quadratic')

        self._matrix = []
        for row_src in src_matrix:
            row_of_transitions = []
            for column_src in row_src:
                transition = self._extract_transition(column_src)
                row_of_transitions.append(transition)
            self._matrix.append(row_of_transitions)

    def __repr__(self):
        return repr(self._matrix)

    def _extract_transition(self, obj_with_two_items):
        """Returns transition object extracted from iterable object.

        If object does not contain two items then function returns None.
        """
        try:
            probability, expectation = obj_with_two_items
        except TypeError:
            transition = None
        else:
            transition = Transition(probability=probability,
                                    expectation=expectation)
        return transition

    def has_only_source_and_drain(self):
        """Returns True if matrix has got only source and drain."""
        matrix_2x2 = len(self._matrix) == 2
        return matrix_2x2 and not self.loop_exists()

    def loop_exists(self):
        """Returns True if loop exists in transition matrix."""
        return self._index_of_first_loop() is None

    def exclude_first_loop(self):
        """Excludes loop from transition matrix."""
        row_loop = column_loop = self._index_of_first_loop()
        try:
            loop = self._matrix[row_loop][column_loop]
        except (TypeError, IndexError):
            raise LoopExcludeError('loop does not found')
        # Loop delete.
        self._matrix[row_loop][column_loop] = None
        # Для исключения петли необходимо поделить вероятности передач,
        # которые находятся на одной строке с петлей, на вероятность петли.
        for (trans_index, trans) in enumerate(self._matrix[row_loop]):
            if trans is not None:
                self._matrix[row_loop][trans_index] = _exclude_loop(trans,
                                                                    loop)

    def exclude_last_vertex(self):
        """Excludes last vertex from transition matrix."""
        # Для исключения узла необходимо умножить передачу из последнего
        # столбца на передачу из последней строки. Произведение поместить на
        # пересечении строки и столбца, сложив его с передачей принимающей
        # ячейки. Например, если в последнем столбце две передачи, а в
        # последней строке три передачи, то получим шесть произведений.
        last_column = last_column_of_matrix(self._matrix)
        last_row = last_row_of_matrix(self._matrix)
        for (column_index, column_trans) in enumerate(last_column):
            for (row_index, row_trans) in enumerate(last_row):
                if column_trans is not None and row_trans is not None:
                    host_cell = self._matrix[column_index][row_index]
                    self._matrix[column_index][row_index] = _exclude_trans(
                        column_trans, row_trans, host_cell)
        # Delete last row from transition matrix.
        self._matrix.pop()
        # Delete last column from transition matrix.
        for row in self._matrix:
            row.pop()

    def _index_of_first_loop(self):
        """Returns index of first loop in transition matrix."""
        for (row_index, row_of_transitions) in enumerate(self._matrix):
            if row_of_transitions[row_index] is not None:
                return row_index


def _exclude_loop(transition, loop):
    probability = transition.probability / (1 - loop.probability)
    expectation = transition.expectation + (
        (loop.expectation * loop.probability) / (1 - loop.probability)
    )
    return Transition(probability=probability, expectation=expectation)


def _exclude_trans(column_trans, row_trans, host_cell=None):
    if host_cell is None:
        host_cell_probability = 0
        host_cell_expectation = 0
    else:
        host_cell_probability = host_cell.probability
        host_cell_expectation = host_cell.expectation
    probability = (column_trans.probability * row_trans.probability
                   + host_cell_probability)
    expectation = (
        (
            host_cell_probability * host_cell_expectation
            + column_trans.probability * row_trans.probability
            * (column_trans.expectation + row_trans.expectation)
        ) / probability
    )
    return Transition(probability=probability, expectation=expectation)

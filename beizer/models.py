# -*- coding: utf-8 -*-
from .exceptions import MatrixInitError
from .utils import matrix_is_quadratic


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
        return "P={0}, E={1}".format(self.probability, self.expectation)


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

    def loop_exists(self):
        """Returns True if loop exists in transition matrix."""

    def exclude_first_loop(self):
        """Excludes loop from transition matrix."""

    def exclude_last_vertex(self):
        """Excludes last vertex from transition matrix."""

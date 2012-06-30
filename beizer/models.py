# -*- coding: utf-8 -*-
from .exceptions import MatrixInitError


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


class TransitionMatrix(object):
    """Transition matrix."""

    def __init__(self, src_matrix):
        """Initializes transition matrix."""
        if not isinstance(src_matrix, list):
            raise MatrixInitError('expected a list object')

        self._matrix = []
        for row_src in src_matrix:
            row_of_transitions = []
            for column_src in row_src:
                probability, expectation = column_src
                transition = Transition(probability=probability,
                                        expectation=expectation)
                row_of_transitions.append(transition)
            self._matrix.append(row_of_transitions)

    def has_only_source_and_drain(self):
        """Returns True if matrix has got only source and drain."""

    def loop_exists(self):
        """Returns True if loop exists in transition matrix."""

    def exclude_first_loop(self):
        """Excludes loop from transition matrix."""

    def exclude_last_vertex(self):
        """Excludes last vertex from transition matrix."""

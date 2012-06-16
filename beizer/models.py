# -*- coding: utf-8 -*-


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
    def __init__(self, matrix):
        """Initializes transition matrix."""
        self._matrix = matrix

    def has_only_source_and_drain(self):
        """Returns True if matrix has got only source and drain."""

    def loop_exists(self):
        """Returns True if loop exists in transition matrix."""

    def exclude_first_loop(self):
        """Excludes loop from transition matrix."""

    def exclude_last_vertex(self):
        """Excludes last vertex from transition matrix."""

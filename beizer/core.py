# -*- coding: utf-8 -*-
from .models import TransitionMatrix


def reduce_matrix_size(transition_matrix):
    """Reduces matrix size."""
    while not transition_matrix.has_only_source_and_drain():
        while transition_matrix.loop_exists():
            transition_matrix.exclude_first_loop()
        transition_matrix.exclude_last_vertex()

if __name__ == '__main__':
    src_matrix = []
    transition_matrix = TransitionMatrix(src_matrix)
    reduce_matrix_size(transition_matrix)

from __future__ import annotations
from enum import Enum
from numpy.random import choice

class Mutation(Enum):
    '''
    A class used to represent an action that may be taken by an actor to mutate the global state

    Methods
    -------
    random(weights: [float]) -> Mutation
        Generates a random mutation according to the provided weight table
    '''

    INJECT = 1
    DISPLAY = 2

    @staticmethod
    def random(weights: [float]) -> Mutation:
        '''Generates a random mutation according to the provided weight table.

        Parameters
        ----------
        weights : [float]
            A list of probabilities corresponding to the outcomes: INJECT | DISPLAY

        Returns
        -------
        Mutation
            The generated mutation
        '''

        return Mutation(choice([Mutation.INJECT, Mutation.DISPLAY], 1, p=weights)[0])

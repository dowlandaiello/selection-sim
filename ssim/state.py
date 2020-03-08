from enum import Enum

class Mutation(Enum):
    '''A class used to represent an action that may be taken by an actor to mutate the global state'''

    INJECT = 1
    DISPLAY = 2

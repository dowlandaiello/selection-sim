from __future__ import annotations
from enum import Enum, unique
from state import Mutation
from typing import Dict
from numpy.random import choice
from random import randrange

class ResponseNet:
    '''
    A class used to represent a logical response pathway, where an environmental condition is treated as an input

    ...

    Attributes
    ----------

    '''

class ResponseNetNode:
    '''
    A class used to represent a conditional logical connection between nodes in a response net

    ...

    Attributes
    ----------
    condition : Condition
        The condition who's activation will result in the execution of this node
    children : [ResponseNetNode]
        The next nodes in the response net; will be activated according to the 
        generating node
    input_modifier : InputModifier
        A functional component that mutates the incoming data, passing on the
        mutated data to child nodes
    resultant_mutation : Mutation
    '''

@unique
class Condition(Enum):
    '''
    A class used to represent a condition upon which the activation of the node will be reliant

    Methods
    -------
    is_active(self, a: int, b: int) -> bool
        Checks whether or not the condition should be active, considering some applicants
    random(weights: [float]) -> Condition
        Generates a random condition according to a provided list of
        probabilities in the following order: EQ, NE, GE, G, LE, L
    '''

    EQ = 1
    NE = 2
    GE = 3
    G = 4
    LE = 5
    L = 6

    def is_active(self, a: int, b: int) -> bool:
        '''Checks if the condition should be activated, considering two applicants.

        Parameters
        ----------
        a : int
            The first applicant to the condition, against which the second applicant will be compared
        b : int
            The second applicant to the condition; will be compared against a

        Returns
        -------
        bool
            Whether or not the condition can be triggered by the provided arguments
        '''

        if self.value == 1:
            return a == b
        elif self.value == 2:
            return a != b
        elif self.value == 3:
            return a >= b
        elif self.value == 4:
            return a > b
        elif self.value == 5:
            return a <= b
        else:
            return a < b

    @staticmethod
    def random(weights: [float]) -> Condition:
        '''Generates a random condition according to a provided weight table.

        Parameters
        ----------
        weights : [float]
            The percentage measured as <= 1 doubles assigned to each possible random condition

        Returns
        -------
        Condition
            The randomly generated condition
        '''

        return Condition(choice([Condition.EQ, Condition.NE, Condition.GE, Condition.G, Condition.LE, Condition.L], 1, p=weights)[0]) 

@unique
class InputModifier(Enum):
    '''
    A class used to represent one of the four arithmetic operations that may be done to an input

    Attributes
    ----------
        applicant : int
            The applicant to the operation (e.g. InputModifier(1, 1) => x + 1, InputModifier(3, 1) => x * 3)

    Methods
    -------
    random(weights: [float]) -> InputModifier
        Generates a random input modifier according to a provided list of
        probabilities in the following order: ADD, SUB, MUL, DIV
    '''

    ADD = 1
    SUB = 2
    MUL = 3
    DIV = 4

    def __init__(self, modifier_id: int, modifier_applicant: int=1.0):
        '''
        Parameters
        ----------
        modifier_id : int
            The number of the desired modifier OP (i.e. ADD => 1, SUB => 2, MUL => 3, DIV => 4)
        modifier_applicant : int
            The applicant to the operation (e.g. InputModifier(1, 1) => x + 1, InputModifier(3, 1) => x * 3)
        '''

        self.applicant = modifier_applicant

    @staticmethod
    def random(weights: [float], max_applicant: int) -> InputModifier:
        '''Generates a random input modifier according to a provided weight table.

        Parameters
        ----------
        weights : [float]
            The percentage measured as <= doubles assigned to each possible random input modifier

        Returns
        -------
        InputModifier
            The randomly generated input modifier
        '''

        return InputModifier(choice([ADD, SUB, MUL, DIV], 1, p=weights)[0], randrange(max_applicant))

    def apply(self, i: int) -> int:
        '''Applies the input modifier to a given input.

        Parameters
        ----------
        i : int
            The input that should be modified by the modifier

        Returns
        -------
        int
            The modified input data
        '''

        if self.value == 1:
            return i + self.applicant
        elif self.value == 2:
            return i - self.applicant
        elif self.value == 3:
            return i * self.applicant
        else:
            return i / self.applicant

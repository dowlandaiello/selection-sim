from __future__ import annotations
from enum import Enum, unique
from state import Mutation
from typing import Dict, List
from numpy.random import choice
from random import randrange
from math import floor

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
    children : List[ResponseNetNode]
        The next nodes in the response net; will be activated according to the 
        generating node
    input_modifier : InputModifier
        A functional component that mutates the incoming data, passing on the
        mutated data to child nodes
    resultant_mutation : Mutation
        The result of hitting the "end" of the response net
    '''

    def __init__(self, condition: Condition, children: List[ResponseNetNode], input_modifier: InputModifier, resultant_mutation: Mutation):
        '''
        Parameters
        ----------
        condition : Condition
            The condition who's activation will result in the execution of this node
        children : List[ResponseNetNode]
            The next nodes in the response net; will be activated according to the 
            generating node
        input_modifier : InputModifier
            A functional component that mutates the incoming data, passing on the
            mutated data to child nodes
        resultant_mutation : Mutation
            The result of hitting the "end" of the response net
        '''
        self.condition = condition
        self.children = children
        self.input_modifier = input_modifier
        self.resultant_mutation = resultant_mutation

    @staticmethod
    def random(condition_weights: List[float], max_children: int, input_modifier_weights: [float], max_input_modifier: int, mutation_weights: [float]) -> ResponseNetNode:
        # Get the number of child nodes that we should generate
        n_children = floor(randrange(max_children))

        # Generate the new node, with its child nodes, recursively
        return ResponseNetNode(
            Condition.random(condition_weights),
            [ResponseNetNode.random(
                condition_weights,
                max_children,
                input_modifier_weights,
                max_input_modifier,
                mutation_weights
            )] * n_children if n_children > 0 else [],
            InputModifier.random(input_modifier_weights, max_input_modifier),
            Mutation.random(mutation_weights)
        )

    def trigger(self, stimulus: int) -> Optional[int]:
        '''Begins resolving the state of the reaction node, considering a stimulus

        Parameters
        ----------
        stimulus : int
            Data fed to the reaction node

        Returns
        -------
        Optional[int]
            Any data returned by the node, or its children
        '''

        # Apply the input modifier to the stimulus
        stimulus = self.input_modifier.apply(stimulus)

        # Activate any applicable children
        for i in range(len(self.children)):
            if self.children[i].condition.is_active(stimulus):
                return self.children[i].trigger(stimulus) 

@unique
class Condition(Enum):
    '''
    A class used to represent a condition upon which the activation of the node will be reliant

    Methods
    -------
    is_active(self, a: int, b: int) -> bool
        Checks whether or not the condition should be active, considering some applicants
    random(weights: List[float]) -> Condition
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
    def random(weights: List[float]) -> Condition:
        '''Generates a random condition according to a provided weight table.

        Parameters
        ----------
        weights : List[float]
            The percentage measured as <= 1 doubles assigned to each possible random condition

        Returns
        -------
        Condition
            The randomly generated condition
        '''

        return Condition(choice([Condition.EQ, Condition.NE, Condition.GE, Condition.G, Condition.LE, Condition.L], 1, p=weights)[0]) 

class ModificationOperation(Enum):
    '''
    A class used to represent one of the four arithmetic operations that may be done to an input

    Methods
    -------
    random(weights: List[floa]) -> InputModifier
        Generates a random modification operation according to a provided list
        of probabilities in the following order: ADD, SUB, MUL, DIV
    '''

    ADD = 1
    SUB = 2
    MUL = 3
    DIV = 4

    @staticmethod
    def random(weights: List[float]) -> ModificationOperation:
        '''Generates a random modification operation according to a provided weight table.

        Parameters
        ----------
        weights : List[float]
            The percentage measured as <= doubles assigned to each possible random input modifier

        Returns
        -------
        ModificationOperation the generated modification operation
        '''

        return ModificationOperation(choice([ModificationOperation.ADD, ModificationOperation.SUB, ModificationOperation.MUL, ModificationOperation.DIV], 1, p=weights)[0])

class InputModifier():
    '''
    A class used to represent one of the four arithmetic operations that may be done to an input

    Attributes
    ----------
    mode : ModificationOperation
        The type of modifier to apply to an input
    applicant : int
        The applicant to the operation (e.g. InputModifier(1, 1) => x + 1, InputModifier(3, 1) => x * 3)

    Methods
    -------
    random(weights: List[float]) -> InputModifier
        Generates a random input modifier according to a provided list of
        probabilities in the following order: ADD, SUB, MUL, DIV
    '''

    def __init__(self, modifier_type: ModificationOperation, modifier_applicant: int=1):
        '''
        Parameters
        ----------
        modifier_id : int
            The number of the desired modifier OP (i.e. ADD => 1, SUB => 2, MUL => 3, DIV => 4)
        modifier_applicant : int
            The applicant to the operation (e.g. InputModifier(1, 1) => x + 1, InputModifier(3, 1) => x * 3)
        '''

        self.mode = modifier_type
        self.applicant = modifier_applicant

    @staticmethod
    def random(weights: List[float], max_applicant: int) -> InputModifier:
        '''Generates a random input modifier according to a provided weight table.

        Parameters
        ----------
        weights : List[float]
            The percentage measured as <= doubles assigned to each possible random input modifier

        Returns
        -------
        InputModifier
            The randomly generated input modifier
        '''

        return InputModifier(ModificationOperation.random(weights), randrange(max_applicant))

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

        if self.mode == ModificationOperation.ADD:
            return i + self.applicant
        elif self.mode == ModificationOperation.SUB:
            return i - self.applicant
        elif self.mode == ModificationOperation.MUL:
            return i * self.applicant
        else:
            return i / self.applicant

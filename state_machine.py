from __future__ import annotations
from abc import ABC, abstractmethod


class Context:
    """
    The Context defines the interface of interest to clients. It also maintains
    a reference to an instance of a State subclass, which represents the current
    state of the Context.
    """

    _state = None
    """
    A reference to the current state of the Context.
    """

    def __init__(self, state: State, command, embedding_store) -> None:
        self.command = command
        self._plan = ""
        self._answer = ""
        self.embedding_store = embedding_store
        self.actions = [""]
        self.transition_to(state)

    def transition_to(self, state: State):
        """
        The Context allows changing the State object at runtime.
        """

        print(f"\nContext: Transition to {type(state).__name__}")
        self._state = state
        self._state.context = self

    """
    The Context delegates part of its behavior to the current State object.
    """

    def run(self):
        self._state.run()

    @property
    def plan(self):
        return self._plan
    
    @plan.setter
    def plan(self, plan):
        print(f"\033[94mContext: updated plan:\n{plan}\033[0m")
        self._plan = plan

    @property
    def answer(self):
        return self._answer
    
    @answer.setter
    def answer(self, answer):
        print(f"\033[92mContext: updated answer: {answer}\033[0m")
        self._answer = answer


class State(ABC):
    """
    The base State class declares methods that all Concrete State should
    implement and also provides a backreference to the Context object,
    associated with the State. This backreference can be used by States to
    transition the Context to another State.
    """

    @property
    def context(self) -> Context:
        return self._context

    @context.setter
    def context(self, context: Context) -> None:
        self._context = context

    @abstractmethod
    def run(self) -> None:
        pass


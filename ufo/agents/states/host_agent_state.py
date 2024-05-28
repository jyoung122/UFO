# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING, Optional, Type

from ufo.agents.agent.app_agent import AppAgent
from ufo.agents.agent.host_agent import HostAgent
from ufo.agents.states.app_agent_state import ContinueAppAgentState
from ufo.agents.states.basic import AgentState, AgentStateManager
from ufo.modules.context import Context

if TYPE_CHECKING:
    from ufo.agents.states.app_agent_state import AppAgentState


class HostAgentStatus(Enum):
    """
    Store the status of the host agent.
    """

    ERROR = "ERROR"
    FINISH = "FINISH"
    CONTINUE = "CONTINUE"
    FAIL = "FAIL"
    PENDING = "PENDING"


class HostAgentStateManager(AgentStateManager):
    """
    The class to manage the states of the host agent.
    """

    @property
    def none_state(self) -> AgentState:
        """
        The none state of the state manager.
        """
        return NoneHostAgentState(self.agent)


class HostAgentState(AgentState):
    """
    The abstract class for the host agent state.
    """

    def create_state_manager(self) -> HostAgentStateManager:
        """
        Create the state manager for the agent.
        """
        return HostAgentStateManager()

    def handle(self, agent: HostAgent, context: Optional["Context"] = None) -> None:
        """
        Handle the agent for the current step.
        :param context: The context for the agent and session.
        """
        pass

    @classmethod
    def agent_class(cls) -> Type[HostAgent]:
        """
        Handle the agent for the current step.
        """
        return HostAgent

    def next_state(self, agent: HostAgent) -> AgentState:
        """
        Get the next state of the agent.
        """
        status = agent.status
        state = HostAgentStateManager.get_state(status)
        return state(agent)

    def next_agent(self, agent: HostAgent) -> HostAgent:
        """
        Get the agent for the next step.
        :param context: The context for the agent and session.
        :return: The agent for the next step.
        """
        return agent


@HostAgentStateManager.register
class FinishHostAgentState(HostAgentState):
    """
    The class for the finish host agent state.
    """

    def is_round_end(self) -> bool:
        """
        Check if the round ends.
        :return: True if the round ends, False otherwise.
        """
        return True

    @classmethod
    def name(cls) -> str:
        """
        The class name of the state.
        """
        return HostAgentStatus.FINISH.value


@HostAgentStateManager.register
class ContinueHostAgentState(HostAgentState):
    """
    The class for the continue host agent state.
    """

    def handle(self, agent: HostAgent, context: Optional["Context"] = None) -> None:
        """
        Handle the agent for the current step.
        :param context: The context for the agent and session.
        """
        agent.process(context)

    def next_state(self, agent: HostAgent) -> AppAgentState:
        """
        Get the next state of the agent.
        :return: The state for the next step.
        """

        # Transition to the app agent state.
        return ContinueAppAgentState

    def next_agent(self, agent: HostAgent) -> AppAgent:
        """
        Get the agent for the next step.
        :param context: The context for the agent and session.
        :return: The agent for the next step.
        """

        # Transition to the app agent.
        return agent.get_active_appagent()

    def is_round_end(self) -> bool:
        """
        Check if the round ends.
        :return: True if the round ends, False otherwise.
        """
        return False

    @classmethod
    def name(cls) -> str:
        """
        The class name of the state.
        """
        return HostAgentStatus.CONTINUE.value


@HostAgentStateManager.register
class PendingHostAgentState(HostAgentState):
    """
    The class for the pending host agent state.
    """

    def is_round_end(self) -> bool:
        """
        Check if the round ends.
        :return: True if the round ends, False otherwise.
        """
        return False

    @classmethod
    def name(cls) -> str:
        """
        The class name of the state.
        """
        return HostAgentStatus.PENDING.value


@HostAgentStateManager.register
class ErrorHostAgentState(HostAgentState):
    """
    The class for the error host agent state.
    """

    def is_round_end(self) -> bool:
        """
        Check if the round ends.
        :return: True if the round ends, False otherwise.
        """
        return True

    @classmethod
    def name(cls) -> str:
        """
        The class name of the state.
        """
        return HostAgentStatus.ERROR.value


@HostAgentStateManager.register
class FailHostAgentState(HostAgentState):
    """
    The class for the fail host agent state.
    """

    def is_round_end(self) -> bool:
        """
        Check if the round ends.
        :return: True if the round ends, False otherwise.
        """
        return True

    @classmethod
    def name(cls) -> str:
        """
        The class name of the state.
        """
        return HostAgentStatus.FAIL.value


@HostAgentStateManager.register
class NoneHostAgentState(HostAgentState):
    """
    The class for the none host agent state.
    """

    def is_round_end(self) -> bool:
        """
        Check if the round ends.
        :return: True if the round ends, False otherwise.
        """
        return True

    @classmethod
    def name(cls) -> str:
        """
        The class name of the state.
        :return: The class name of the state.
        """
        return ""

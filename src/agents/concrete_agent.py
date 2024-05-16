"""
agents/concrete_agent.py

This module represents a concrete agent that extends the AutonomousAgent blueprint.
It provides additional functionality specific to concrete agents.

1. Message Handling:
   - The agent consumes messages from its inbox and filters them for the keyword "hello."
   - If a message contains "hello," the entire message is printed to stdout.

2. Behavior Execution:
   - The agent runs a behavior that generates random 2-word messages.
   - The words are selected from an alphabet of 10 predefined words:
    "hello," "sun," "world," "space," "moon," "crypto," "sky," "ocean," "universe," and "human."
   - The behavior repeats every 2 seconds.

"""

import logging
import random

from configs.config import ALPHABET
from lib.utility import process_data
from models.message import Message

from .autonomous_agent import AutonomousAgent


class ConcreteAgent(AutonomousAgent):
    """
    This class represents a concrete agent that extends the AutonomousAgent blueprint.

    Attributes:
        All parent class attributes i.e. of AutonomousAgent class.

    Methods:
        handle_custom_message(message): Handles an incoming custom message.
        generate_random_message(): Generates a random custom message.
    """

    def __init__(self):
        """
        Initializes a ConcreteAgent instance by extending the AutonomousAgent and
        guides its workflow.

        Args:
            None

        Returns:
            None
        """
        super().__init__()

        # Get: 'msg_type' and 'agent_id'.
        # Note: this is designed in a way that these can be passed from main.
        input_msg_type = "custom"
        input_agent_id = Message.generate_agent_id()
        self.agent_id = process_data(input_agent_id)
        self.msg_type = (
            Message.DEFAULT_TYPE if process_data(input_msg_type) is None else input_msg_type
        )
        self.msg_type = (
            "custom" if not (self.msg_type == Message.DEFAULT_TYPE) else Message.DEFAULT_TYPE
        )

        self.register_message_handler(self.msg_type, self.handle_custom_message)
        self.register_behavior(self.generate_random_message)
        logging.info(f"Invoking Agent: {self.agent_id}.")

    async def handle_custom_message(self, message):
        """
        Handles an incoming custom message containing data about message and agent.

        Args:
            message (class Message): The incoming message.

        Returns:
            None
        """
        if "hello" in message.content:
            logging.info(
                f"Received '{message.type}' message '{message.content}' from '{message.agent_id}'."
            )

    async def generate_random_message(self) -> None:
        """
        Generates a random custom message by selecting two words from an alphabet list.
        """
        message_content = process_data(" ".join(random.sample(ALPHABET, 2)))
        message = Message(self.agent_id, type=self.msg_type, content=message_content)
        await self.emit_message(message)

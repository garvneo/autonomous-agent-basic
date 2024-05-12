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
        self.register_message_handler("custom", self.handle_custom_message)
        self.register_behavior(self.generate_random_message)

    async def handle_custom_message(self, message):
        """
        Handles an incoming custom message containing the word "hello".

        Args:
            message (dict): The incoming message.

        Returns:
            None
        """
        if "hello" in message["content"]:
            logging.info(f"Received message: {message}")

    async def generate_random_message(self) -> None:
        """
        Generates a random custom message by selecting two words from an alphabet list.

        Args:
            None

        Returns:
            None
        """
        message = " ".join(random.sample(ALPHABET, 2))
        await self.emit_message({"type": "custom", "content": message})

"""
agents/autonomous_agent.py

This module represents an autonomous agent that can act as a blueprint for creating
agents with specific behaviors. It provides the following features:

1. Message Exchange:
   - The agent has an inbox and an outbox for message exchange with other agents.
   - By connecting outboxes and inboxes, you can create communication channels
     between agents.

2. Message Handling:
   - The agent consumes messages from its inbox and handles them based on their types.
   - You can register custom message handlers to react to specific message types.

3. Behavior Execution:
   - The agent runs behaviors periodically (e.g., every 2 seconds).
   - Behaviors can be proactive (triggered by internal state or local time) and allow
     the agent to create new messages.
"""

import asyncio
import logging

from configs.config import BEHAVIOUR_INTERVAL, CONSUME_INTERVAL
from lib.exception import IncorrectMessageContentException, IncorrectMessageFormatException
from models.message import Message


class AutonomousAgent:
    """
    Represents an autonomous agent with message handling and behavior execution.

    Attributes:
        inbox (asyncio.Queue): Queue for incoming messages.
        outbox (asyncio.Queue): Queue for outgoing messages.
        message_handlers (dict): Dictionary mapping message types to handler functions.
        behaviors (list): List of behavior functions.
        behavior_interval = time in sec
        consume_interval = time in sec

    Methods:
        consume_messages(): Continuously consumes messages from the inbox.
        handle_message(message): Handles an incoming message using the appropriate handler.
        emit_message(message): Adds a message to the outbox.
        register_message_handler(message_type, handler): Registers a message handler.
        register_behavior(behavior): Registers a behavior function.
        run_behaviors(): Executes registered behaviors periodically.
    """

    def __init__(self):
        self.inbox = asyncio.Queue()
        self.outbox = asyncio.Queue()
        self.message_handlers = {}
        self.behaviors = []
        self.behavior_interval = BEHAVIOUR_INTERVAL
        self.consume_interval = CONSUME_INTERVAL

    async def consume_messages(self):
        """
        Continuously consumes messages from the inbox.
        """
        while True:
            try:
                message = await self.inbox.get()
                await self.handle_message(message)
                await asyncio.sleep(self.consume_interval)
            except asyncio.CancelledError:
                logging.info("Message consumption task cancelled.")
                break
            except Exception as e:
                logging.exception(f"Error consuming message: {e}")

    async def handle_message(self, message):
        """
        Handles an incoming message using the appropriate handler.

        Args:
            message (class Message): The incoming message.

        Returns:
            None
        """
        try:
            if not isinstance(message, Message):
                raise IncorrectMessageFormatException(
                    "Received message is not in correct format, skipping further processing."
                )
            elif len(message.content.split(" ")) != 2:
                msg = (
                    f"Received wrong message content:'{message.content}' from '{message.agent_id}',"
                    "\nit should have only 2 words separated with a single space.\n"
                    "Skipping further processing."
                )
                raise IncorrectMessageContentException(msg)
        except (IncorrectMessageFormatException, IncorrectMessageContentException) as e:
            logging.warning(e)
            return  # Skip: processing incorrect messages

        # Note: If message is intance of Message class then automatically it becomes ready for
        # preprocessing as it will hold proper values of all required attributes hence no recheck.
        handler = self.message_handlers.get(message.type)

        if handler:
            try:
                await handler(message)
            except Exception as e:
                logging.exception(f"Error in handling message: {message.content}\n{e}")

    async def emit_message(self, message):
        """
        Adds a message to the outbox.

        Args:
            message (dict): The message to emit.

        Returns:
            None
        """
        try:
            if self.outbox.full():
                logging.warning("Outbox is full. Message has been dropped.")
            else:
                await self.outbox.put(message)
        except Exception as e:
            logging.exception("Error emitting message: %s", e)

    def register_message_handler(self, message_type, handler):
        """
        Registers a message handler.

        Args:
            message_type (str): The type of message.
            handler (callable): The handler function.

        Returns:
            None
        """
        try:
            self.message_handlers[message_type] = handler
        except Exception as e:
            logging.error(f"Error occurred while registering message handler: {e}")

    def register_behavior(self, behavior):
        """
        Registers a behavior function.

        Args:
            behavior (callable): The behavior function.

        Returns:
            None
        """
        try:
            self.behaviors.append(behavior)
        except Exception as e:
            logging.error(f"Error occurred while registering behavior: {e}")

    async def run_behaviors(self):
        """
        Executes registered behaviors periodically.

        Returns:
            None
        """
        while True:
            try:
                for behavior in self.behaviors:
                    await behavior()
                await asyncio.sleep(self.behavior_interval)
            except asyncio.CancelledError:
                logging.info("Behavior execution task cancelled.")
                break
            except Exception as e:
                logging.exception(f"Error running behaviors: {e}")

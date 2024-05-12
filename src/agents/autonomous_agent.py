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


class AutonomousAgent:
    """
    Represents an autonomous agent with message handling and behavior execution.

    Attributes:
        inbox (asyncio.Queue): Queue for incoming messages.
        outbox (asyncio.Queue): Queue for outgoing messages.
        message_handlers (dict): Dictionary mapping message types to handler functions.
        behaviors (list): List of behavior functions.

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

    async def consume_messages(self):
        """
        Continuously consumes messages from the inbox.
        """
        while True:
            message = await self.inbox.get()
            await self.handle_message(message)

    async def handle_message(self, message):
        """
        Handles an incoming message using the appropriate handler.

        Args:
            message (dict): The incoming message.

        Returns:
            None
        """
        handler = self.message_handlers.get(message["type"])
        if handler:
            await handler(message)

    async def emit_message(self, message):
        """
        Adds a message to the outbox.

        Args:
            message (dict): The message to emit.

        Returns:
            None
        """
        await self.outbox.put(message)

    def register_message_handler(self, message_type, handler):
        """
        Registers a message handler.

        Args:
            message_type (str): The type of message.
            handler (callable): The handler function.

        Returns:
            None
        """
        self.message_handlers[message_type] = handler

    def register_behavior(self, behavior):
        """
        Registers a behavior function.

        Args:
            behavior (callable): The behavior function.

        Returns:
            None
        """
        self.behaviors.append(behavior)

    async def run_behaviors(self):
        """
        Executes registered behaviors periodically.

        Returns:
            None
        """
        while True:
            for behavior in self.behaviors:
                await behavior()
            await asyncio.sleep(2)

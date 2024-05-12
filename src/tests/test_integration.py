""" tests/test_integration.py
This module does integration testing using standard library unittest.
"""

import asyncio
import unittest

from agents.concrete_agent import ConcreteAgent


class TestIntegration(unittest.IsolatedAsyncioTestCase):
    async def test_agents_communication(self):
        """
        This method does integration testing.
        """
        agent1 = ConcreteAgent()
        agent2 = ConcreteAgent()
        agent1.outbox = asyncio.Queue()
        agent2.outbox = asyncio.Queue()

        # Set: up communication between agents
        agent1.outbox = agent2.inbox
        agent2.outbox = agent1.inbox

        # Start: consuming messages and running behaviors
        asyncio.create_task(agent1.consume_messages())
        asyncio.create_task(agent2.consume_messages())
        asyncio.create_task(agent1.run_behaviors())
        asyncio.create_task(agent2.run_behaviors())

        # Emit: a message from agent1 and check if agent2 receives it
        message_from_agent1 = {"type": "custom", "content": "hello world"}
        await agent1.emit_message(message_from_agent1)
        received_message = await agent2.inbox.get()
        self.assertEqual(message_from_agent1, received_message)

        # Emit: a message from agent2 and check if agent1 receives it
        message_from_agent2 = {"type": "custom", "content": "foo bar"}
        await agent2.emit_message(message_from_agent2)
        received_message = await agent1.inbox.get()
        self.assertEqual(message_from_agent2, received_message)


if __name__ == "__main__":
    unittest.main()

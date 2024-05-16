"""tests/test_integration.py
This module does integration testing using standard library unittest.
"""

import asyncio
import unittest

from agents.concrete_agent import ConcreteAgent
from models.message import Message


class TestIntegration(unittest.IsolatedAsyncioTestCase):
    TIME_INTERVAL = 1

    async def test_agents_communication(self):
        """
        This method does integration testing.
        """
        agent1 = ConcreteAgent()
        agent2 = ConcreteAgent()
        agent1.outbox = asyncio.Queue()
        agent2.outbox = asyncio.Queue()

        # Set up communication between agents
        agent1.outbox = agent2.inbox
        agent2.outbox = agent1.inbox

        # Start consuming messages and running behaviors
        tasks = [
            asyncio.create_task(agent1.consume_messages()),
            asyncio.create_task(agent2.consume_messages()),
            asyncio.create_task(agent1.run_behaviors()),
            asyncio.create_task(agent2.run_behaviors()),
        ]

        # Testing explicit message exchange with agent_id
        agent1_id = Message.generate_agent_id()
        agent2_id = Message.generate_agent_id()

        message_from_agent1 = Message(agent_id=agent1_id, type="custom", content="hello world")
        await agent1.emit_message(message_from_agent1)
        received_message = await agent2.inbox.get()
        self.assertEqual(message_from_agent1.type, received_message.type)
        self.assertEqual(message_from_agent1.content, received_message.content)
        self.assertEqual(message_from_agent1.agent_id, received_message.agent_id)

        message_from_agent2 = Message(agent_id=agent2_id, type="default", content="foo bar")
        await agent2.emit_message(message_from_agent2)
        received_message = await agent1.inbox.get()
        self.assertEqual(message_from_agent2.type, received_message.type)
        self.assertEqual(message_from_agent2.content, received_message.content)
        self.assertEqual(message_from_agent2.agent_id, received_message.agent_id)

        # Testing: proactiveness
        await asyncio.sleep(self.TIME_INTERVAL)

        proactiveness_message_agent1 = await agent1.inbox.get()
        self.assertIsNotNone(proactiveness_message_agent1)
        # Check: message structure
        self.assertTrue(hasattr(proactiveness_message_agent1, "type"))
        self.assertTrue(hasattr(proactiveness_message_agent1, "content"))
        self.assertTrue(hasattr(proactiveness_message_agent1, "agent_id"))

        # Validate: message content has exactly two words
        words = proactiveness_message_agent1.content.split()
        self.assertEqual(len(words), 2)

        proactiveness_message_agent2 = await agent2.inbox.get()
        self.assertIsNotNone(proactiveness_message_agent2)
        self.assertTrue(hasattr(proactiveness_message_agent2, "type"))
        self.assertTrue(hasattr(proactiveness_message_agent2, "content"))
        self.assertTrue(hasattr(proactiveness_message_agent2, "agent_id"))

        # Validate: message content has exactly two words
        words = proactiveness_message_agent2.content.split()
        self.assertEqual(len(words), 2)

        # Stop: tasks (optional)
        for task in tasks:
            task.cancel()


if __name__ == "__main__":
    unittest.main()

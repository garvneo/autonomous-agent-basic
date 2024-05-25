"""tests/test_unittest.py
This module does unit testing on main functionalitie susing standard library unittest
and in one case utilizes parameterized library too.
"""

import asyncio
import unittest
from unittest.mock import MagicMock, patch

from parameterized import parameterized

from agents.autonomous_agent import AutonomousAgent
from agents.concrete_agent import ConcreteAgent
from models.message import Message


class TestConcreteAgent(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.agent = ConcreteAgent()

    async def test_initialization(self):
        self.assertIsNotNone(self.agent)
        self.assertIsNotNone(self.agent.agent_id)
        self.assertIsNotNone(self.agent.msg_type)
        self.assertTrue(hasattr(self.agent, "handle_custom_message"))
        self.assertTrue(hasattr(self.agent, "generate_random_message"))

    @parameterized.expand(
        [
            [{"type": "custom", "content": "hello world"}, True],
            [{"type": "custom", "content": "random message"}, False],
            [{"type": "default", "content": "david v"}, False],
            [{"type": "", "content": "None"}, False],
            [{"agent_id": "agent_50", "type": "default", "content": "world hello"}, True],
            [{"content": "random sniper"}, False],
            [{"agent_id": "agent_42", "type": "default", "content": "garv neo"}, False],
            [{"type": "custom", "content": "None"}, False],
        ]
    )
    async def test_handle_custom_message(self, message_data, expected_call):
        message = Message(**message_data)
        with patch("agents.concrete_agent.logging.info") as mock_logging_info:
            await self.agent.handle_custom_message(message)
            expected_message = (
                f"Received '{message.type}' message '{message.content}' from '{message.agent_id}'."
            )
            if expected_call:
                mock_logging_info.assert_called_once_with(expected_message)
            else:
                mock_logging_info.assert_not_called()

    async def test_generate_random_message(self):
        with patch(
            "agents.concrete_agent.random.sample", return_value=["hello", "world"]
        ), patch.object(self.agent, "emit_message") as mock_emit_message:
            await self.agent.generate_random_message()
            mock_emit_message.assert_called_once()

    async def test_emit_message(self):
        message = Message(type="custom", content="test message")
        await self.agent.emit_message(message)
        self.assertFalse(self.agent.outbox.empty())


class TestAutonomousAgent(unittest.IsolatedAsyncioTestCase):
    async def test_handle_message_positive(self):
        agent = AutonomousAgent()
        message = Message(content="hello world")
        await agent.handle_message(message)

    async def test_handle_message_incorrect_format(self):
        agent = AutonomousAgent()
        message = "invalid message"
        with patch("agents.autonomous_agent.logging.warning") as mock_logging_warning:
            await agent.handle_message(message)
            mock_logging_warning.assert_called_once()

    async def test_handle_message_incorrect_content(self):
        agent = AutonomousAgent()
        message = Message(content="hello world foo")
        with patch("agents.autonomous_agent.logging.warning") as mock_logging_warning:
            await agent.handle_message(message)
            mock_logging_warning.assert_called_once()

    async def test_emit_message_positive(self):
        agent = AutonomousAgent()
        message = Message()
        await agent.emit_message(message)
        # No assertion needed, as the method should not raise any exceptions

    async def test_emit_message_queue_full(self):
        agent = AutonomousAgent()
        agent.outbox = asyncio.Queue(maxsize=1)
        await agent.outbox.put("Some message")
        message = Message()
        with patch("agents.autonomous_agent.logging.warning") as mock_logging_warning:
            await agent.emit_message(message)
            mock_logging_warning.assert_called_once()

    def test_register_message_handler_positive(self):
        agent = AutonomousAgent()
        message_type = "custom"
        handler = MagicMock()
        agent.register_message_handler(message_type, handler)
        self.assertIn(message_type, agent.message_handlers)
        self.assertEqual(agent.message_handlers[message_type], handler)

    def test_register_behavior_positive(self):
        agent = AutonomousAgent()
        behavior = MagicMock()
        agent.register_behavior(behavior)
        self.assertIn(behavior, agent.behaviors)


if __name__ == "__main__":
    unittest.main()

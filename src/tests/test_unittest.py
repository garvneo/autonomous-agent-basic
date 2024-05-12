""" tests/test_unittest.py
This module does unit testing on main functionalitiesusing standard library unittest.
"""
import unittest
from unittest.mock import patch

from agents.concrete_agent import ConcreteAgent


class TestConcreteAgent(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.agent = ConcreteAgent()

    async def test_handle_custom_message(self):
        """
        This method tests the handling of incoming messages.
        """
        message_with_hello = {"type": "custom", "content": "hello world"}
        message_without_hello = {"type": "custom", "content": "random message"}

        # Testing: message with "hello"
        with patch("agents.concrete_agent.logging.info") as mock_logging_info:
            await self.agent.handle_custom_message(message_with_hello)
            mock_logging_info.assert_called_once_with(f"Received message: {message_with_hello}")

        # Testing: message without "hello"
        with patch("agents.concrete_agent.logging.info") as mock_logging_info:
            await self.agent.handle_custom_message(message_without_hello)
            mock_logging_info.assert_not_called()

    async def test_generate_random_message(self):
        """
        This method test the generation fo random two word messages.
        """
        with patch("agents.concrete_agent.random.sample", return_value=["hello", "world"]):
            with patch.object(self.agent, "emit_message") as mock_emit_message:
                await self.agent.generate_random_message()
                mock_emit_message.assert_called_once_with(
                    {"type": "custom", "content": "hello world"}
                )


if __name__ == "__main__":
    unittest.main()

"""models/message.py
This module holds the message class and its attributes for proper Message handling.
"""

import random

from configs.config import MAX_AGENT
from lib.utility import process_data


class Message:
    AGENT_ID_PREFIX = "agent"
    DEFAULT_TYPE = "default"
    DEFAULT_CONTENT = ""
    AGENT_IDS = set()

    def __init__(self, agent_id=None, type=None, content=None):
        self.agent_id = agent_id if agent_id else self.generate_agent_id()
        self.type = type if process_data(type) else self.DEFAULT_TYPE
        self.content = content if content else self.DEFAULT_CONTENT

    @staticmethod
    def generate_agent_id():
        """
        Generate a unique agent ID.

        Returns:
            str: A unique agent ID generated using the AGENT_ID_PREFIX
            followed by a random integer between 1 and MAX_AGENT + 1.

        """
        while True:
            name = f"{Message.AGENT_ID_PREFIX}_{random.randint(1, MAX_AGENT + 1)}"
            if name not in Message.AGENT_IDS:
                Message.AGENT_IDS.add(name)
                return name

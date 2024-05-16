"""
main.py

This script demonstrates the interaction between two concrete instances of an Autonomous Agent.
The agents exchange messages through their outboxes and inboxes, running behaviors concurrently.
Keyboard interrupts are handled and is one of the ways to stop the program execution.
"""

import asyncio
import logging

from agents.concrete_agent import ConcreteAgent


async def main():
    """
    Creates two instances of ConcreteAgent, connects their outboxes to each other's inboxes,
    and starts message consumption and behavior execution concurrently.

    Returns:
        None
    """
    try:
        # Create: two instances of ConcreteAgent
        logging.info("Preparing the agents.")
        agent1 = ConcreteAgent()
        agent2 = ConcreteAgent()

        # Connect: the agents outboxes to each other's inboxes
        agent1.outbox = agent2.inbox
        agent2.outbox = agent1.inbox

        # Start: consuming messages and running behaviors for each agent
        logging.info("Starting the agents with:")
        logging.info("behaviour: to generate random 2-word messages.")
        logging.info(
            "handler: to filters messages for the keyword 'hello' and then print it's content."
        )
        tasks = [
            asyncio.create_task(agent1.consume_messages()),
            asyncio.create_task(agent2.consume_messages()),
            asyncio.create_task(agent1.run_behaviors()),
            asyncio.create_task(agent2.run_behaviors()),
        ]

        # Wait: for all tasks to complete
        await asyncio.gather(*tasks)

    except KeyboardInterrupt:
        logging.info("Stopping the agents.")
        for task in tasks:
            task.cancel()
    except Exception as e:
        logging.exception(f"Oops! Our agents are down as: {e}")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="[%(asctime)s] %(levelname)s - %(message)s")
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info("Stopping the agents.")
    except Exception as e:
        logging.exception(f"Oops! Our agents are down as: {e}")

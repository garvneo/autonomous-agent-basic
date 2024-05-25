### IMP: MUST VISIT - The upgraded version of this project which is live on internet. This upgrade handles the agent trigger and stop functionality through an asynchronous web app.
- **Autonomous Agent (Upgraded App): [Live site link](https://autonomous-agents.onrender.com/)**
- **Autonomous Agent (Upgraded App): [Source code & readme.md link](https://github.com/garvneo/autonomous-agents)**
- PR of advance app was not raised for review because to make it live on internet it was needed to be pushed and merged to default branch.
  
# Autonomous Agents (autonomous-agent-basic)

This project demonstrates the implementation of autonomous agents which are capable of 
communicating and executing behaviors asynchronously.

## Design:

### Basic Implementation
- Picked 'asyncio' standard library of python to implement this project. 
- Created a folder named 'agents'.
- Developed a module 'agents\autonomous_agent.py' as a blueprint for the 'Autonomous Agent', addressing its reactivity, proactivity, behaviors, and asynchronous message handling.
- Implemented a module 'agents\concrete_agent.py' which somewhat follows the blueprint of 'Autonomous Agent' or inherits 'agents\autonomous_agent.py'.
- Utilized 'Queue' data structure to manage messages in InBoxes and OutBoxes, and dictionaries and lists for message handlers and behaviors, respectively.
- Created a simple 'app.py' acting as a controller, where instances of concrete classes were created, their inboxes linked to outboxes, and behaviors invoked asynchronously, enabling agents to communicate asynchronously.
- Developed unit and integration test cases using Python's standard library 'Unittest'.


### Best practices followed:
1. Utilized 'Ruff' for making code more Pythonic and also added 'ruff.toml' to ensure that same rules of linting & formatting can be followed by all who will be contributing to the project.
2. Ensured modular code design for increased maintainability and scalability.
3. Incorporated test cases for ensuring better project delivery.
4. Exception handling has been utilized for more robustness.
5. Incorporated logging which can come very handy in debugging production failures and also in multiple other scenarios.

## Tech Stack
- Python & its Standard Libraries.
- 'Ruff' for linting and auto-formatting.

## Usage
1. Navigate to the directory containing 'main.py' and run the following command in the terminal:
    ```
    python main.py
    ```
2. Run test cases as scripts:
    ```
    python -m unittest tests.test_unittest
    ```
    ```
    python -m unittest tests.test_integration
    ```
3. Expected output example:
    ```
    [2024-05-13 01:05:08,696] INFO - Preparing the agents.
    [2024-05-13 01:05:08,696] INFO - Starting the agents with:
    [2024-05-13 01:05:08,696] INFO - behaviour: to generate random 2-word messages.
    [2024-05-13 01:05:08,696] INFO - handler: to filters messages for the keyword 'hello' and then print it's content.
    [2024-05-13 01:05:08,696] INFO - Received message: {'type': 'custom', 'content': 'space hello'}
    [2024-05-13 01:05:22,740] INFO - Received message: {'type': 'custom', 'content': 'hello moon'}
    [2024-05-13 01:05:24,755] INFO - Received message: {'type': 'custom', 'content': 'hello ocean'}
    [2024-05-13 01:05:26,763] INFO - Received message: {'type': 'custom', 'content': 'sun hello'}
    [2024-05-13 01:05:28,766] INFO - Received message: {'type': 'custom', 'content': 'hello world'}
    [2024-05-13 01:05:32,775] INFO - Received message: {'type': 'custom', 'content': 'hello human'}
    [2024-05-13 01:05:36,793] INFO - Received message: {'type': 'custom', 'content': 'sky hello'}
    [2024-05-13 01:05:44,253] INFO - Stopping the agents.
    ```

## More Information
For further details and documentation, please visit this [GitHub repository](https://github.com/garvneo/autonomous-agents)** of mine.

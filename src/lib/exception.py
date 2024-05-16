"""lib/exception.py
Holds custom exception classes for various use cases.
"""


class IncorrectAgentIdentifierException(Exception):
    """Exception raised for incorrect agent identifiers.

    Attributes:
        message - explanation of the error
    """

    def __init__(self, message="Incorrect agent identifier format."):
        self.message = message
        super().__init__(self.message)


class IncorrectMessageFormatException(Exception):
    """Exception raised for incorrect message format.

    Attributes:
        message - explanation of the error
    """

    def __init__(self, message="Incorrect message format."):
        self.message = message
        super().__init__(self.message)


class IncorrectMessageContentException(Exception):
    """Exception raised for incorrect message content.

    Attributes:
        message - explanation of the error
    """

    def __init__(self, message="Incorrect message content."):
        self.message = message
        super().__init__(self.message)

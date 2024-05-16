"""lib/utility.py
Hold utility function which can be needed to be called in different modules.
"""

import re


def process_data(data):
    """Process the input data by removing leading and trailing whitespace,
    replacing multiple spaces with a single space, and then replacing internal
    whitespace with None.

    Args:
        data (str): The input data to be processed.

    Returns:
        str or None: The processed data if it's not empty or None, otherwise None.
    """
    cleaned_data = re.sub(r"^\s+|\s+$", "", data) if data is not None else None
    cleaned_data = re.sub(r"\s+", " ", cleaned_data) if cleaned_data is not None else None
    cleaned_data = None if cleaned_data in ["", None] else cleaned_data
    return cleaned_data

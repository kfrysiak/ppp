from pathlib import Path


def get_test_directory() -> Path:
    """
    Returns the path to the test directory.
    """
    return Path(__file__).parent

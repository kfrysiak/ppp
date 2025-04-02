from pathlib import Path
from unittest.mock import Mock
from rich.console import Console

from ppp.toml_service import Script, extract_scripts
from ppp.tests.lib import get_test_directory


def get_scripts() -> list[Script]:
    return [
        Script(
            name="docker-up",
            command="docker run -it -v bob:the_builder nvm",
            comments=["Run a docker image with http server"],
            inline_comment="[start|stop]",
        ),
        Script(
            name="type",
            command="echo",
            comments=[],
            inline_comment="text",
        ),
        Script(
            name="shell",
            command="echo $SHELL",
            comments=[],
            inline_comment="text",
        ),
    ]


def test() -> None:
    config = get_test_directory() / "test_pyproject.toml"
    mock_console = Mock(spec=Console)  # Create a mock Console
    scripts: list[Script] = extract_scripts(
        Path(config),
        console=mock_console,
    )
    assert scripts == get_scripts()
    print("scripts", scripts)

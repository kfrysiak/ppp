from pathlib import Path
import re
from typing import Optional
from dataclasses import dataclass
import toml
from rich.console import Console


@dataclass
class Script:
    name: str
    comments: list[str]
    inline_comment: Optional[str]
    command: Optional[str]


header_pattern = re.compile(r"^\s*\[(.*?)\]\s*$")
key_pattern = re.compile(r"""^([^\s=]+)\s*=.*(?<!['\"]).*""")
comment_pattern = re.compile(r"""(#.*)$""")

TOOL_HEADER = "tool"
PPP_HEADER = "ppp"
SCRIPTS_HEADER = "scripts"
FULL_HEADER = f"{TOOL_HEADER}.{PPP_HEADER}.{SCRIPTS_HEADER}"


def extract_toml_headers(line: str) -> Optional[str]:
    match = header_pattern.match(line)
    if not match:
        return None
    return match.group(1).strip()


def extract_comment(line: str) -> Optional[str]:
    if line.startswith("#"):
        return line[1:].strip()
    return None


def unwrap_quotes(key: str) -> str:
    """Unwraps quotes from the key if they are present."""
    if key.startswith("'") and key.endswith("'"):
        return key[1:-1]
    elif key.startswith('"') and key.endswith('"'):
        return key[1:-1]
    return key


def extract_entry(line: str) -> Optional[tuple[str, Optional[str]]]:
    """If entry is detected, return its key and optional inline comment as a tuple."""
    match = key_pattern.match(line)
    if not match:
        return None
    key = match.group(1).strip()
    key = unwrap_quotes(key)
    if key.startswith(("'", '"')) and key.endswith(("'", '"')):
        key = key[1:-1]

    comment_match = comment_pattern.search(line)

    if not comment_match:
        return (key, None)

    inline_comment = comment_match.group(0)
    if inline_comment is not None:
        inline_comment = inline_comment[1:].strip()
    return (key, inline_comment)


def extract_scripts(file_path: Path, console: Console) -> list[Script]:
    """
    Extracts scripts from tool.pp.scripts section within pyproject TOML file, returning a
    list of Script objects.
    """
    found_header: bool = False
    comments: list[str] = []
    scripts: list[Script] = []

    with open(file_path, "r") as file:
        for line in file:
            line = line.strip()
            if not found_header:
                header = extract_toml_headers(line)
                if header is not None and header.startswith(FULL_HEADER):
                    found_header = True
                continue
            else:
                if line.strip() == "" or extract_toml_headers(line) is not None:
                    # Reached the end of the scripts section or a new header
                    break
            comment = extract_comment(line)
            if comment:
                # It's a comment, aggregate it for the next script
                comments.append(comment)
                continue
            entry = extract_entry(line)
            if entry is not None:
                key, inline_comment = entry
                script = Script(
                    name=key,
                    comments=comments,
                    inline_comment=inline_comment,
                    command=None,
                )
                comments = []
                scripts.append(script)

    # I won't write a TOML parser, and we can't trust regex to parse TOML correctly. So we
    # use toml library and match the scripts by keys
    with open(file_path, "r") as file:
        toml_data = toml.load(file)
        toml_scripts = (
            toml_data.get(TOOL_HEADER, {}).get(PPP_HEADER, {}).get(SCRIPTS_HEADER, None)
        )
        if toml_scripts is None:
            console.print(
                "Specify your scripts in [bold][tool.ppp.scripts][/bold] section in [bold]pyproject.toml[/bold]"
            )
            return []
        for key, value in toml_scripts.items():
            for script in scripts:
                if script.name == key:
                    script.command = value
                    break
    return scripts

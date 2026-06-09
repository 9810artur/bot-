"""Text formatting utilities."""


def escape_markdown(text: str) -> str:
    """Escape markdown special characters."""
    special_chars = ["_", "*", "[", "]", "(", ")", "~", "`", ">", "#", "+", "-", "=", "|", "{", "}", ".", "!"]
    for char in special_chars:
        text = text.replace(char, f"\\{char}")
    return text


def bold(text: str) -> str:
    """Make text bold."""
    return f"*{escape_markdown(text)}*"


def italic(text: str) -> str:
    """Make text italic."""
    return f"_{escape_markdown(text)}_"


def code(text: str) -> str:
    """Format text as code."""
    return f"`{escape_markdown(text)}`"


def code_block(text: str, language: str = "") -> str:
    """Format text as code block."""
    return f"```{language}\n{text}\n```"


def link(text: str, url: str) -> str:
    """Create link."""
    return f"[{escape_markdown(text)}]({url})"

def escaped_markdown(text: str) -> str:
    # Standard Markdown characters that need to be escaped + extended characters.
    _MARKDOWN_CHARACTERS_TO_ESCAPE = set(r"\`*_{}[]<>()#+-.!|" + "~^")
    return "".join(
        f"\\{character}" if character in _MARKDOWN_CHARACTERS_TO_ESCAPE else character for character in text
    )

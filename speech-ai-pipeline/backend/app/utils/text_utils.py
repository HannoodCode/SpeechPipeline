import re
import html


def strip_html_tags(text: str) -> str:
    """Remove HTML tags from text."""
    if not text:
        return ""
    # Remove script and style blocks
    text = re.sub(r"<\s*(script|style)[^>]*>[\s\S]*?<\s*/\s*\1\s*>", " ", text, flags=re.IGNORECASE)
    # Remove all remaining tags
    text = re.sub(r"<[^>]+>", " ", text)
    return text


def strip_markdown(text: str) -> str:
    """Remove common Markdown syntax while preserving readable text."""
    if not text:
        return ""
    # Images: ![alt](url) -> alt
    text = re.sub(r"!\[([^\]]*)\]\([^)]*\)", r"\1", text)
    # Links: [text](url) -> text
    text = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", text)
    # Inline code: `code` -> code
    text = re.sub(r"`([^`]+)`", r"\1", text)
    # Code blocks: ```lang\ncode\n``` -> code
    text = re.sub(r"```[\s\S]*?```", " ", text)
    # Bold/italic markers
    text = re.sub(r"\*\*|__|\*|_", "", text)
    # Headers, blockquotes, lists
    text = re.sub(r"^\s{0,3}#{1,6}\s*", "", text, flags=re.MULTILINE)
    text = re.sub(r"^\s{0,3}>\s?", "", text, flags=re.MULTILINE)
    text = re.sub(r"^\s*[-*+]\s+", "", text, flags=re.MULTILINE)
    text = re.sub(r"^\s*\d+\.\s+", "", text, flags=re.MULTILINE)
    return text


def normalize_whitespace(text: str) -> str:
    """Collapse consecutive whitespace into single spaces and trim."""
    if not text:
        return ""
    text = html.unescape(text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def strip_all_markup(text: str) -> str:
    """Strip HTML and Markdown, unescape entities, and normalize whitespace."""
    return normalize_whitespace(strip_markdown(strip_html_tags(text)))


def escape_ssml(text: str) -> str:
    """Escape characters that are unsafe in SSML content nodes."""
    if not text:
        return ""
    # First unescape any existing entities to avoid double-escaping oddities
    text = html.unescape(text)
    # Then escape XML special characters
    text = (text
            .replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
            .replace('"', "&quot;")
            .replace("'", "&apos;"))
    return text



#!/usr/bin/env python3
"""
ASCII Callout Quote Generator
Creates memorable, shareable ASCII art blocks for blog quotes.

Usage:
    uv run ascii_callout.py "Your quote here" --author "Author Name" --style provocative

Styles:
    - classic: Standard double-line box
    - provocative: Bold borders with lightning emoji
    - insight: Rounded corners with lightbulb
    - data: Single-line box for metrics
    - warning: Heavy borders with warning emoji
"""

import argparse
import textwrap
from typing import Literal

Style = Literal["classic", "provocative", "insight", "data", "warning"]


def wrap_text(text: str, width: int = 60) -> list[str]:
    """Wrap text to specified width."""
    return textwrap.wrap(text, width=width)


def generate_classic(quote: str, author: str = "", width: int = 65) -> str:
    """Classic double-line box style."""
    lines = wrap_text(quote, width - 6)
    inner_width = width - 2

    result = []
    result.append("╔" + "═" * inner_width + "╗")
    result.append("║" + " " * inner_width + "║")

    for line in lines:
        padded = f"   {line}".ljust(inner_width)
        result.append(f"║{padded}║")

    result.append("║" + " " * inner_width + "║")

    if author:
        author_line = f"— {author}".rjust(inner_width - 3)
        result.append(f"║{author_line}   ║")
        result.append("║" + " " * inner_width + "║")

    result.append("╚" + "═" * inner_width + "╝")

    return "\n".join(result)


def generate_provocative(quote: str, author: str = "", width: int = 65) -> str:
    """Bold borders with lightning emoji for controversial takes."""
    lines = wrap_text(quote, width - 6)
    inner_width = width - 2

    result = []
    result.append("┏" + "━" * inner_width + "┓")
    result.append("┃  ⚡ CONTROVERSIAL TAKE ⚡" + " " * (inner_width - 26) + "┃")
    result.append("┃" + " " * inner_width + "┃")

    for line in lines:
        padded = f"  {line}".ljust(inner_width)
        result.append(f"┃{padded}┃")

    result.append("┃" + " " * inner_width + "┃")

    if author:
        author_line = f"— {author}".rjust(inner_width - 2)
        result.append(f"┃{author_line}  ┃")

    result.append("┗" + "━" * inner_width + "┛")

    return "\n".join(result)


def generate_insight(quote: str, author: str = "", width: int = 60) -> str:
    """Rounded corners with lightbulb for aha moments."""
    lines = wrap_text(quote, width - 8)
    inner_width = width - 2

    result = []
    result.append("    ╭" + "─" * (inner_width - 4) + "╮")
    result.append("    │" + " " * (inner_width - 4) + "│")
    result.append("    │  💡 " + " " * (inner_width - 9) + "│")

    for line in lines:
        padded = f"  {line}".ljust(inner_width - 4)
        result.append(f"    │{padded}│")

    result.append("    │" + " " * (inner_width - 4) + "│")

    if author:
        result.append("    │      This changes everything." + " " * (inner_width - 38) + "│")
        result.append("    │" + " " * (inner_width - 4) + "│")

    result.append("    ╰" + "─" * (inner_width - 4) + "╯")

    return "\n".join(result)


def generate_data(metrics: list[tuple[str, str]], title: str = "THE NUMBERS DON'T LIE", width: int = 65) -> str:
    """Single-line box for data/metrics display."""
    inner_width = width - 2

    result = []
    result.append("┌" + "─" * inner_width + "┐")

    title_line = f"  📊 {title}"
    result.append(f"│{title_line.ljust(inner_width)}│")
    result.append("│" + " " * inner_width + "│")

    for label, value in metrics:
        metric_line = f"  {label}: {value}"
        result.append(f"│{metric_line.ljust(inner_width)}│")

    result.append("│" + " " * inner_width + "│")
    result.append("└" + "─" * inner_width + "┘")

    return "\n".join(result)


def generate_warning(quote: str, author: str = "", width: int = 65) -> str:
    """Heavy borders with warning emoji."""
    lines = wrap_text(quote, width - 6)
    inner_width = width - 2

    result = []
    result.append("╔" + "═" * inner_width + "╗")
    result.append("║  ⚠️  WARNING" + " " * (inner_width - 14) + "║")
    result.append("║" + " " * inner_width + "║")

    for line in lines:
        padded = f"  {line}".ljust(inner_width)
        result.append(f"║{padded}║")

    result.append("║" + " " * inner_width + "║")

    if author:
        author_line = f"— {author}".rjust(inner_width - 2)
        result.append(f"║{author_line}  ║")

    result.append("╚" + "═" * inner_width + "╝")

    return "\n".join(result)


def generate_callout(
    quote: str,
    style: Style = "classic",
    author: str = "",
    width: int = 65,
    metrics: list[tuple[str, str]] | None = None,
    title: str = ""
) -> str:
    """Generate ASCII callout in specified style."""

    if style == "classic":
        return generate_classic(quote, author, width)
    elif style == "provocative":
        return generate_provocative(quote, author, width)
    elif style == "insight":
        return generate_insight(quote, author, width)
    elif style == "data":
        if metrics:
            return generate_data(metrics, title or "THE NUMBERS DON'T LIE", width)
        return generate_data([("Value", quote)], title, width)
    elif style == "warning":
        return generate_warning(quote, author, width)
    else:
        return generate_classic(quote, author, width)


def save_callout(content: str, filepath: str) -> None:
    """Save callout to file."""
    with open(filepath, 'w') as f:
        f.write(content)


def main():
    parser = argparse.ArgumentParser(description="Generate ASCII art callout quotes")
    parser.add_argument("quote", help="The quote text")
    parser.add_argument("--author", "-a", default="", help="Quote author")
    parser.add_argument("--style", "-s", default="classic",
                       choices=["classic", "provocative", "insight", "data", "warning"],
                       help="Callout style")
    parser.add_argument("--width", "-w", type=int, default=65, help="Box width")
    parser.add_argument("--output", "-o", help="Output file path")
    parser.add_argument("--title", "-t", default="", help="Title for data style")

    args = parser.parse_args()

    callout = generate_callout(
        quote=args.quote,
        style=args.style,
        author=args.author,
        width=args.width,
        title=args.title
    )

    print(callout)

    if args.output:
        save_callout(callout, args.output)
        print(f"\nSaved to: {args.output}")


if __name__ == "__main__":
    main()

"""Logging utilities for the application."""
import logging
from rich.console import Console
from rich.panel import Panel
from rich.style import Style as RichStyle
from rich.text import Text
from ..config.constants import CUSTOM_THEME

# Initialize console
console = Console(theme=CUSTOM_THEME, stderr=True)
console.quiet = True

# Style configurations
error_style = RichStyle(color="red", bold=True)
success_style = RichStyle(color="green", bold=True)
info_style = RichStyle(color="cyan")
warning_style = RichStyle(color="yellow")
highlight_style = RichStyle(color="magenta", bold=True)

def print_status(message: str, status_type: str = "info", transient: bool = False) -> None:
    """Print a streamlined status message with rich styling."""
    styles = {
        "info": info_style,
        "success": success_style,
        "error": error_style,
        "warning": warning_style,
        "processing": highlight_style,
        "debug": RichStyle(color="bright_black"),
    }
    prefix_map = {
        "info": "➜",
        "success": "✓",
        "error": "✗",
        "warning": "⚠",
        "processing": "⟳",
        "debug": "DEBUG",
    }
    style = styles.get(status_type)
    prefix = prefix_map.get(status_type, "➜")
    
    with PRINT_LOCK:
        if transient:
            console.print(f"\r{prefix} {message}", style=style, end="\r")
        else:
            console.print(f"{prefix} {message}", style=style)

def print_error(error: Exception, context: str = "") -> None:
    """Print formatted error message without stacktrace."""
    error_type = type(error).__name__
    error_msg = str(error).split("\n")[0]
    if context:
        console.print(f"{context}: {error_type} - {error_msg}", style="error")
    else:
        console.print(f"{error_type} - {error_msg}", style="error")
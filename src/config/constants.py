"""Configuration constants for the application."""
import os
from rich.theme import Theme

# Windows API Constants
PROCESS_QUERY_INFORMATION = 0x0400
PROCESS_VM_READ = 0x0010
HANDLE_FLAG_INHERIT = 0x00000001
HANDLE_FLAG_PROTECT_FROM_CLOSE = 0x00000002

# Application Constants
HEADER_WIDTH = 70
MAX_BATCH_SIZE = 3
MAX_OPEN_TABS = 15
MIN_CHAT_LIFETIME = 60
MAX_RETRIES = 3

# Timeouts
BATCH_TIMEOUT = 10
RECONNECT_TIMEOUT = 10
ORDER_TIMEOUT = 3
CLEANUP_TIMEOUT = 60
RETRY_DELAY = 2
STALE_RETRY_DELAY = 1
CONNECTION_RETRY_DELAY = 5

# UI Elements
SUCCESS_SYMBOL = "✓ "
ERROR_SYMBOL = "✗ "
ARROW_SYMBOL = "➜ "
PROCESSING_SYMBOL = "⟳ "
INPUT_SYMBOL = "▶ "
DEBUG_SYMBOL = "⚙ "

# Chat Related
STALE_CHAT_TEXT = "Still need help with your issue?"
ACTIVE_CHAT_INDICATORS = ["agent-typing", "queue-position", "chat-message"]

# Theme Configuration
CUSTOM_THEME = Theme({
    "info": "cyan",
    "success": "green bold",
    "error": "red bold",
    "warning": "yellow",
    "processing": "magenta",
    "debug": "dim white",
    "highlight": "magenta bold",
    "header": "blue bold",
    "accent": "cyan",
    "muted": "dim white",
})
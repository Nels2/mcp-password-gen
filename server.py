from typing import Any
import httpx
import json
from mcp.server.fastmcp import FastMCP
from datetime import datetime
import string
import random

mcp = FastMCP("mcp-password-generator")

# Complexity mode definitions
CHARSETS = {
    "simple": string.ascii_letters + string.digits,
    "strong": string.ascii_letters + string.digits + "!@#$%^&*()-_=+",
    "maximum": ''.join(c for c in string.printable if c not in ' \t\n\r\x0b\x0c')
}

@mcp.tool()
async def generate_password(length: int = 12, complexity: str = "strong") -> str:
    """
    Generates a secure random password.

    Args:
        length (int): The desired length of the password (default: 12). Max 1024.
        complexity (str): One of 'simple', 'strong', or 'maximum'.

    Returns:
        str: The generated password in JSON format.
    """
    if not (1 <= length <= 1024):
        return json.dumps({"error": "Password length must be between 1 and 1024."})

    if complexity not in CHARSETS:
        return json.dumps({"error": f"Invalid complexity mode. Choose from: {', '.join(CHARSETS.keys())}"})

    charset = CHARSETS[complexity]
    unique_charset = list(set(charset))

    
    required = [
        random.choice(string.ascii_lowercase),
        random.choice(string.ascii_uppercase),
        random.choice(string.digits),
    ]

    remaining_length = length - len(required)
    password_chars = []

    if remaining_length <= len(set(charset)) - len(required):
        available = [c for c in set(charset) if c not in required]
        password_chars = random.sample(available, k=remaining_length)
    else:
        password_chars = random.choices(charset, k=remaining_length)

    password_chars += required
    random.shuffle(password_chars)
    return json.dumps({"password": ''.join(password_chars)})


if __name__ == "__main__":
    mcp.run(transport='stdio')
    # command to run this mcp-server from terminal for use with open-webui: ` uvx mcpo --port 5086 -- uv run 03_mcpserver.py `

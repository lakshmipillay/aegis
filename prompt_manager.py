import os

import os
import shutil

# Original baked-in prompt
DEFAULT_PROMPT_FILE = "system_prompt.txt"
# Writable location for Cloud Run
WRITABLE_PROMPT_FILE = "/tmp/system_prompt.txt"

def get_system_prompt():
    """Reads the current system prompt, preferring the updated one in /tmp."""
    try:
        # Check if we have a patched version
        if os.path.exists(WRITABLE_PROMPT_FILE):
            with open(WRITABLE_PROMPT_FILE, "r") as f:
                return f.read().strip()
                
        # Fallback to the original baked-in prompt
        if os.path.exists(DEFAULT_PROMPT_FILE):
            with open(DEFAULT_PROMPT_FILE, "r") as f:
                return f.read().strip()
                
        return "You are a helpful assistant."
    except Exception as e:
        print(f"Error reading system prompt: {e}")
        return "You are a helpful assistant."

def update_system_prompt(new_prompt):
    """Updates the system prompt by writing to /tmp (since /app is read-only)."""
    try:
        with open(WRITABLE_PROMPT_FILE, "w") as f:
            f.write(new_prompt)
        print(f"System prompt updated successfully at {WRITABLE_PROMPT_FILE}.")
        return True
    except Exception as e:
        print(f"Error updating system prompt: {e}")
        return False

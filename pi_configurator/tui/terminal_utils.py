"""
Terminal Utilities

Handles terminal input in raw mode for better arrow key support.
"""

import os
import sys
import tty
import termios
import select
from typing import Optional

class TerminalInput:
    """Handles terminal input with arrow key support."""
    
    def __init__(self):
        self.fd = sys.stdin.fileno()
        self.old_settings = None
    
    def __enter__(self):
        """Enter raw mode."""
        self.old_settings = termios.tcgetattr(self.fd)
        tty.setraw(sys.stdin.fileno())
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Exit raw mode."""
        if self.old_settings:
            termios.tcsetattr(self.fd, termios.TCSADRAIN, self.old_settings)
    
    def get_key(self, timeout: float = 0.1) -> Optional[str]:
        """Get a single key press with timeout."""
        if select.select([sys.stdin], [], [], timeout)[0]:
            key = sys.stdin.read(1)
            
            # Handle escape sequences (arrow keys, etc.)
            if key == '\x1b':
                # Read next two bytes for complete escape sequence
                if select.select([sys.stdin], [], [], timeout)[0]:
                    key2 = sys.stdin.read(1)
                    if key2 == '[':
                        if select.select([sys.stdin], [], [], timeout)[0]:
                            key3 = sys.stdin.read(1)
                            return f'\x1b[{key2}{key3}'
                return '\x1b'
            
            return key
        return None

def get_user_choice(max_option: int, prompt: str = "Select option: ") -> str:
    """Get user choice with basic input handling."""
    try:
        # Try enhanced input with arrow key support
        print(prompt, end='', flush=True)
        
        choice = ''
        with TerminalInput() as term_input:
            while True:
                key = term_input.get_key()
                
                if key is None:
                    continue
                
                # Handle arrow keys
                elif key == '\x1b[A':  # Up arrow
                    print('↑', end='', flush=True)
                    return 'UP'
                elif key == '\x1b[B':  # Down arrow
                    print('↓', end='', flush=True)
                    return 'DOWN'
                
                # Handle Enter
                elif key == '\r' or key == '\n':
                    print()
                    return choice
                
                # Handle Backspace
                elif key == '\x7f' or key == '\x08':
                    if choice:
                        choice = choice[:-1]
                        print('\b \b', end='', flush=True)
                
                # Handle regular characters
                elif key.isdigit() or key.lower() in ['q', '?', 'h']:
                    print(key, end='', flush=True)
                    choice += key
                
                # Ignore other keys
                
    except (termios.error, AttributeError):
        # Fallback to simple input if terminal doesn't support raw mode
        return input(prompt).strip()

if __name__ == "__main__":
    # Test the terminal input
    print("Testing terminal input (press q to quit):")
    try:
        with TerminalInput() as term_input:
            while True:
                key = term_input.get_key()
                if key:
                    if key == 'q':
                        print("\nQuitting...")
                        break
                    print(f"Got: {repr(key)}")
    except Exception as e:
        print(f"Terminal raw mode not supported: {e}")
        print("Falling back to simple input")
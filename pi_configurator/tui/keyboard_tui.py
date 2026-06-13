"""
Keyboard-based TUI

Uses the keyboard library for reliable arrow key support.
"""

import os
import sys
from typing import Dict, Any, List, Optional
from pi_configurator.core.config_manager import ConfigManager

try:
    import keyboard
    KEYBOARD_AVAILABLE = True
except ImportError:
    KEYBOARD_AVAILABLE = False

class KeyboardTUI:
    """TUI using keyboard library for navigation."""
    
    def __init__(self, config_manager: ConfigManager):
        """Initialize the keyboard TUI."""
        self.config_manager = config_manager
        self.current_menu = "main"
        self.menus = self._build_menus()
        self.current_selection = 0
        self.running = True
    
    def _build_menus(self) -> Dict[str, Dict]:
        """Build the menu structure."""
        return {
            "main": {
                "title": "Pi-Ckl Configuration",
                "items": [
                    ("Model & AI Settings", "model", "Configure AI models and providers"),
                    ("UI & Display", "ui", "Theme, layout and visual settings"),
                    ("System & Performance", "system", "Compaction, retry and delivery settings"),
                    ("Resources & Extensions", "resources", "Manage extensions, skills and packages"),
                    ("Bedrock Pricing", "bedrock", "AWS Bedrock tier configuration"),
                    ("View Configuration", "view", "View current settings"),
                    ("Save & Exit", "save", "Save configuration and exit"),
                    ("Exit Without Saving", "exit", "Exit without saving changes")
                ]
            },
            # Add other menus as needed...
        }
    
    def _clear_screen(self):
        """Clear the screen."""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def _show_menu(self):
        """Show the current menu."""
        menu = self.menus[self.current_menu]
        print("=" * 70)
        print(f"🎛️  {menu['title']}".center(70))
        print("=" * 70)
        
        items = menu["items"]
        for i, (text, action, description) in enumerate(items, 1):
            if i == self.current_selection + 1:
                print(f"▶ {i}. {text}")
                print(f"   {description}")
            else:
                print(f"  {i}. {text}")
                print(f"   {description}")
        
        print("-" * 70)
        print("Navigation: ↑↓ arrows, Enter to select, q to quit, ? for help")
        print("-" * 70)
    
    def _handle_keyboard_input(self) -> Optional[str]:
        """Handle keyboard input with arrow key support."""
        if not KEYBOARD_AVAILABLE:
            return input("Select option: ").strip().lower()
        
        print("Select option: ", end='', flush=True)
        
        while True:
            try:
                event = keyboard.read_event()
                
                # Handle arrow keys
                if event.event_type == keyboard.KEY_DOWN:
                    if event.name == 'up':
                        print('↑', end='', flush=True)
                        return 'UP'
                    elif event.name == 'down':
                        print('↓', end='', flush=True)
                        return 'DOWN'
                    elif event.name == 'enter':
                        print()
                        return 'ENTER'
                    elif event.name == 'q':
                        return 'q'
                    elif event.name == '?':
                        return '?'
                    elif event.name.isdigit():
                        print(event.name, end='', flush=True)
                        return event.name
                
            except KeyboardInterrupt:
                return None
            except Exception:
                # Fallback to simple input
                return input().strip().lower()
    
    def run(self) -> None:
        """Run the keyboard TUI."""
        try:
            while self.running:
                self._clear_screen()
                self._show_menu()
                
                choice = self._handle_keyboard_input()
                if choice is None:
                    break
                
                choice = choice.lower()
                
                # Handle arrow key navigation
                if choice == 'up':
                    self.current_selection = max(0, self.current_selection - 1)
                    continue
                elif choice == 'down':
                    self.current_selection = min(len(self.menus[self.current_menu]["items"]) - 1, self.current_selection + 1)
                    continue
                
                # Handle special commands
                elif choice in ['q', 'quit', 'exit']:
                    self.running = False
                    break
                
                elif choice in ['?', 'help']:
                    self._show_help()
                    continue
                
                # Handle numeric selection
                elif choice.isdigit():
                    selection = int(choice) - 1
                    items = self.menus[self.current_menu]["items"]
                    if 0 <= selection < len(items):
                        text, action, description = items[selection]
                        self._handle_action(action)
                        continue
                
                print("❌ Invalid option. Please try again.")
                input("Press Enter to continue...")
            
        except Exception as e:
            print(f"Error: {e}")
        finally:
            if KEYBOARD_AVAILABLE:
                keyboard.unhook_all()
            print("\n👋 Thank you for using Pi-Ckl!")
    
    def _show_help(self):
        """Show help."""
        print("\n📖 Pi-Ckl Help")
        print("=" * 70)
        print("""
NAVIGATION:
  ↑↓ arrows      - Move selection up/down
  Enter         - Select current item
  q or quit     - Quit current menu
  ? or help     - Show this help

EDITING:
  Follow prompts to edit values
  Changes are applied immediately
  Use 'Save & Exit' to persist changes

Press Enter to continue...
""")
        input()
    
    def _handle_action(self, action: str):
        """Handle menu actions."""
        if action == "main":
            self.current_menu = "main"
            self.current_selection = 0
        
        elif action == "save":
            self.config_manager.save_settings()
            self.running = False
            print("\n✅ Configuration saved successfully!")
        
        elif action == "exit":
            self.running = False
            print("\n❌ Exited without saving.")
        
        elif action == "view":
            self._clear_screen()
            self.config_manager.list_settings()
            input("\nPress Enter to continue...")
        
        # Add other action handlers as needed...

class KeyboardTUIHandler:
    """Handler for keyboard TUI."""
    
    def __init__(self, config_manager: ConfigManager):
        self.config_manager = config_manager
    
    def run(self) -> None:
        """Run the keyboard TUI."""
        if not KEYBOARD_AVAILABLE:
            print("Keyboard library not available, falling back to simple TUI...")
            from pi_configurator.tui.simple_tui_handler import SimpleTUIHandler
            simple_tui = SimpleTUIHandler(self.config_manager)
            simple_tui.run()
            return
        
        try:
            tui = KeyboardTUI(self.config_manager)
            tui.run()
        except Exception as e:
            print(f"Keyboard TUI failed: {e}")
            print("Falling back to simple TUI...")
            from pi_configurator.tui.simple_tui_handler import SimpleTUIHandler
            simple_tui = SimpleTUIHandler(self.config_manager)
            simple_tui.run()
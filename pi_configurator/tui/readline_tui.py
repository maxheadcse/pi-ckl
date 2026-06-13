"""
Readline-based TUI

Uses GNU readline for better input handling with arrow key support.
"""

import os
import sys
from typing import Dict, Any, List, Optional
import readline
from pi_configurator.core.config_manager import ConfigManager

class ReadlineTUI:
    """TUI using GNU readline for navigation."""
    
    def __init__(self, config_manager: ConfigManager):
        """Initialize the readline TUI."""
        self.config_manager = config_manager
        self.current_menu = "main"
        self.menus = self._build_menus()
        self.current_selection = 0
        self.running = True
        self._setup_readline()
    
    def _setup_readline(self):
        """Setup readline for better input."""
        # Custom tab completion
        readline.parse_and_bind('tab: complete')
        readline.parse_and_bind('set editing-mode vi')
        
        # Custom key bindings would go here
        # For now, we'll handle navigation with numbers
    
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
        print("Navigation: Use numbers (1-9) to select, q to quit, ? for help")
        print("-" * 70)
    
    def _handle_input(self) -> Optional[str]:
        """Handle user input."""
        try:
            choice = input("Select option: ").strip()
            return choice
        except (EOFError, KeyboardInterrupt):
            return None
    
    def run(self) -> None:
        """Run the readline TUI."""
        try:
            while self.running:
                self._clear_screen()
                self._show_menu()
                
                choice = self._handle_input()
                if choice is None:
                    break
                
                choice = choice.lower()
                
                # Handle special commands
                if choice in ['q', 'quit', 'exit']:
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
            print("\n👋 Thank you for using Pi-Ckl!")
    
    def _show_help(self):
        """Show help."""
        print("\n📖 Pi-Ckl Help")
        print("=" * 70)
        print("""
NAVIGATION:
  1-9          - Select menu option directly
  q or quit    - Quit current menu
  ? or help    - Show this help

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

class ReadlineTUIHandler:
    """Handler for readline TUI."""
    
    def __init__(self, config_manager: ConfigManager):
        self.config_manager = config_manager
    
    def run(self) -> None:
        """Run the readline TUI."""
        try:
            tui = ReadlineTUI(self.config_manager)
            tui.run()
        except Exception as e:
            print(f"Readline TUI failed: {e}")
            print("Falling back to simple TUI...")
            from pi_configurator.tui.simple_tui_handler import SimpleTUIHandler
            simple_tui = SimpleTUIHandler(self.config_manager)
            simple_tui.run()
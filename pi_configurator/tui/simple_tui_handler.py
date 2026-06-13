"""
Simple Terminal User Interface Handler
Fallback when curses is not available or fails
"""

import os
import sys
from typing import Dict, Any
from pi_configurator.core.config_manager import ConfigManager

class SimpleTUIHandler:
    """Simple Terminal User Interface Handler."""
    
    def __init__(self, config_manager: ConfigManager):
        """Initialize the simple TUI handler."""
        self.config_manager = config_manager
        self.current_menu = "main"
        self.menus = self._build_menus()
        self.current_selection = 0
        self.running = True
        
        # Initialize terminal
        self._setup_terminal()
    
    def _setup_terminal(self):
        """Setup terminal for better UX."""
        # Try to get terminal size
        try:
            self.terminal_size = os.get_terminal_size()
            self.width = self.terminal_size.columns
            self.height = self.terminal_size.lines
        except:
            self.width = 80
            self.height = 24
    
    def _build_menus(self) -> Dict[str, Dict]:
        """Build the menu structure."""
        return {
            "main": {
                "title": "Pi Coding Agent Configuration",
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
            "model": {
                "title": "Model & AI Settings",
                "items": [
                    ("Default Provider", "provider", f"Current: {self.config_manager.get_provider()}"),
                    ("Default Model", "model", f"Current: {self.config_manager.settings.get('model', {}).get('defaultModel', 'Not set')}"),
                    ("Thinking Level", "thinking", f"Current: {self.config_manager.get_thinking_level()}"),
                    ("Hide Thinking Block", "thinking_block", f"Current: {self.config_manager.settings.get('model', {}).get('hideThinkingBlock', False)}"),
                    ("Back to Main Menu", "main", "Return to main menu")
                ]
            },
            "ui": {
                "title": "UI & Display Settings",
                "items": [
                    ("Theme", "theme", f"Current: {self.config_manager.get_theme()}"),
                    ("Quiet Startup", "quiet", f"Current: {self.config_manager.settings.get('ui', {}).get('quietStartup', False)}"),
                    ("Project Trust", "trust", f"Current: {self.config_manager.settings.get('ui', {}).get('defaultProjectTrust', 'ask')}"),
                    ("Back to Main Menu", "main", "Return to main menu")
                ]
            },
            "system": {
                "title": "System & Performance",
                "items": [
                    ("Compaction Settings", "compaction", "Configure message compaction"),
                    ("Retry Settings", "retry", "Configure retry behavior"),
                    ("Message Delivery", "delivery", "Configure message delivery"),
                    ("Back to Main Menu", "main", "Return to main menu")
                ]
            },
            "resources": {
                "title": "Resources & Extensions",
                "items": [
                    ("Packages", "packages", f"Current: {self.config_manager.settings.get('resources', {}).get('packages', [])}"),
                    ("Extensions", "extensions", f"Current: {self.config_manager.settings.get('resources', {}).get('extensions', [])}"),
                    ("Skills", "skills", f"Current: {self.config_manager.settings.get('resources', {}).get('skills', [])}"),
                    ("Back to Main Menu", "main", "Return to main menu")
                ]
            },
            "bedrock": {
                "title": "Bedrock Pricing Configuration",
                "items": [
                    ("Default Tier", "tier", f"Current: {self.config_manager.get_bedrock_tier()}"),
                    ("Back to Main Menu", "main", "Return to main menu")
                ]
            }
        }
    
    def _clear_screen(self):
        """Clear the screen."""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def _draw_header(self):
        """Draw the header."""
        menu_title = self.menus[self.current_menu]["title"]
        print("=" * self.width)
        print(f"🎛️  {menu_title}".center(self.width))
        print("=" * self.width)
        print()
    
    def _draw_menu(self):
        """Draw the current menu."""
        menu_items = self.menus[self.current_menu]["items"]
        
        for i, (text, action, description) in enumerate(menu_items):
            if i == self.current_selection:
                print(f"▶ {i+1}. {text}")
                print(f"   {description}")
            else:
                print(f"  {i+1}. {text}")
                print(f"   {description}")
            print()
    
    def _draw_footer(self):
        """Draw the footer."""
        print("-" * self.width)
        print("Navigation: ↑↓ arrows or j/k to move, Enter to select, q to quit, ? for help")
        print("-" * self.width)
    
    def _handle_input(self):
        """Handle user input."""
        menu_items = self.menus[self.current_menu]["items"]
        
        # Get user input
        user_input = input("Select option: ").strip().lower()
        
        # Handle special commands
        if user_input in ['q', 'quit', 'exit']:
            if self.current_menu == "main":
                self.running = False
                return "exit"
            else:
                self.current_menu = "main"
                self.current_selection = 0
                return "back"
        
        elif user_input in ['?', 'help']:
            self._show_help()
            return "help"
        
        # Handle numeric selection
        elif user_input.isdigit():
            selection = int(user_input) - 1
            if 0 <= selection < len(menu_items):
                self.current_selection = selection
                text, action, description = menu_items[selection]
                return action
        
        # Handle arrow keys (simple fallback)
        elif user_input in ['j', '↓']:
            self.current_selection = min(len(menu_items) - 1, self.current_selection + 1)
            return "navigate"
        
        elif user_input in ['k', '↑']:
            self.current_selection = max(0, self.current_selection - 1)
            return "navigate"
        
        return "unknown"
    
    def _show_help(self):
        """Show help screen."""
        self._clear_screen()
        print("📖 Pi Configurator - Help")
        print("=" * self.width)
        print("""
NAVIGATION:
  ↑↓ arrows or j/k  - Move selection up/down
  Enter            - Select current item
  q or quit        - Quit current menu
  ? or help        - Show this help

EDITING:
  Follow the prompts to edit values
  Changes are applied immediately
  Use 'Save & Exit' to persist changes

MAIN MENU SHORTCUTS:
  1-8              - Select menu options
  save             - Save configuration and exit
  exit             - Exit without saving

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
            print("🎉 Thank you for using Pi Configurator!")
        
        elif action == "exit":
            self.running = False
            print("\n❌ Exited without saving.")
        
        elif action == "view":
            self._clear_screen()
            self.config_manager.list_settings()
            input("\nPress Enter to continue...")
        
        elif action == "provider":
            self._edit_provider()
        
        elif action == "tier":
            self._edit_bedrock_tier()
        
        elif action == "theme":
            self._edit_theme()
        
        # Add more action handlers as needed
    
    def _edit_provider(self):
        """Edit the AI provider."""
        providers = ["anthropic", "openai", "google", "aws-bedrock"]
        current = self.config_manager.get_provider()
        
        self._clear_screen()
        print("🤖 Edit AI Provider")
        print("=" * self.width)
        print(f"Current provider: {current}\n")
        
        for i, provider in enumerate(providers, 1):
            marker = "▶" if provider == current else " "
            print(f"{marker} {i}. {provider}")
        
        print(f"\nSelect provider (1-{len(providers)} or name): ", end="")
        choice = input().strip()
        
        if choice.isdigit() and 1 <= int(choice) <= len(providers):
            new_provider = providers[int(choice) - 1]
        elif choice in providers:
            new_provider = choice
        else:
            print("❌ Invalid provider")
            input("Press Enter to continue...")
            return
        
        self.config_manager.settings.setdefault('model', {})['defaultProvider'] = new_provider
        print(f"\n✅ Provider set to: {new_provider}")
        input("Press Enter to continue...")
        
        # Rebuild menus to update current values
        self.menus = self._build_menus()
    
    def _edit_bedrock_tier(self):
        """Edit Bedrock pricing tier."""
        tiers = ["flex", "standard", "spot"]
        current = self.config_manager.get_bedrock_tier()
        
        self._clear_screen()
        print("💰 Edit Bedrock Pricing Tier")
        print("=" * self.width)
        print(f"Current tier: {current}\n")
        print("Available tiers:")
        print("  ▶ 1. flex      - Pay per request (recommended)")
        print("     2. standard - Pay per vCPU-second")
        print("     3. spot     - Cheapest, but can be interrupted")
        
        print(f"\nSelect tier (1-3 or name): ", end="")
        choice = input().strip()
        
        if choice == "1" or choice.lower() == "flex":
            new_tier = "flex"
        elif choice == "2" or choice.lower() == "standard":
            new_tier = "standard"
        elif choice == "3" or choice.lower() == "spot":
            new_tier = "spot"
        else:
            print("❌ Invalid tier")
            input("Press Enter to continue...")
            return
        
        self.config_manager.settings.setdefault('bedrock', {})['defaultTier'] = new_tier
        print(f"\n✅ Bedrock tier set to: {new_tier}")
        
        if new_tier == "flex":
            print("💡 Tip: 'flex' tier is pay-per-request, recommended for variable workloads")
        elif new_tier == "standard":
            print("💡 Tip: 'standard' tier is pay-per-vCPU-second, for consistent workloads")
        else:
            print("💡 Tip: 'spot' tier is cheapest but instances can be interrupted")
        
        input("Press Enter to continue...")
        
        # Rebuild menus to update current values
        self.menus = self._build_menus()
    
    def _edit_theme(self):
        """Edit theme setting."""
        themes = ["dark", "light", "system"]
        current = self.config_manager.get_theme()
        
        self._clear_screen()
        print("🎨 Edit Theme")
        print("=" * self.width)
        print(f"Current theme: {current}\n")
        
        for i, theme in enumerate(themes, 1):
            marker = "▶" if theme == current else " "
            print(f"{marker} {i}. {theme}")
        
        print(f"\nSelect theme (1-{len(themes)} or name): ", end="")
        choice = input().strip()
        
        if choice.isdigit() and 1 <= int(choice) <= len(themes):
            new_theme = themes[int(choice) - 1]
        elif choice in themes:
            new_theme = choice
        else:
            print("❌ Invalid theme")
            input("Press Enter to continue...")
            return
        
        self.config_manager.settings.setdefault('ui', {})['theme'] = new_theme
        print(f"\n✅ Theme set to: {new_theme}")
        input("Press Enter to continue...")
        
        # Rebuild menus to update current values
        self.menus = self._build_menus()
    
    def run(self) -> None:
        """Run the simple TUI."""
        try:
            while self.running:
                self._clear_screen()
                self._draw_header()
                self._draw_menu()
                self._draw_footer()
                
                action = self._handle_input()
                
                if action in ["exit", "back", "help", "navigate", "unknown"]:
                    continue
                
                self._handle_action(action)
            
        except KeyboardInterrupt:
            print("\n\n❌ Operation cancelled by user.")
        except Exception as e:
            print(f"\n\n❌ Error: {e}")
        finally:
            print("\n👋 Thank you for using Pi Configurator!")
"""
Modern Terminal User Interface using Rich
Provides a professional, interactive configuration experience
"""

import os
import sys
from typing import Dict, Any, List, Optional
from rich.console import Console
from rich.panel import Panel
from rich.layout import Layout
from rich.live import Live
from rich.style import Style
from rich.text import Text
from rich.prompt import Prompt, Confirm
from rich.table import Table
from rich.box import ROUNDED
from pi_configurator.core.config_manager import ConfigManager

# Conditional imports for platform-specific functionality
try:
    if os.name == 'nt':
        import msvcrt
    else:
        import tty, termios
        msvcrt = None
except ImportError:
    msvcrt = None

class ModernTUI:
    """Modern Terminal User Interface using Rich."""
    
    def __init__(self, config_manager: ConfigManager):
        """Initialize the modern TUI."""
        self.config_manager = config_manager
        self.console = Console()
        self.current_menu = "main"
        self.running = True
        self.menus = self._build_menus()
    
    def _build_menus(self) -> Dict[str, Dict]:
        """Build the menu structure."""
        return {
            "main": {
                "title": "🎛️  Pi-Ckl Configuration",
                "description": "Configure your AI assistant settings",
                "items": [
                    ("🤖 Model & AI Settings", "model", "Configure AI models and providers"),
                    ("🎨 UI & Display", "ui", "Theme, layout and visual settings"),
                    ("⚙️  System & Performance", "system", "Compaction, retry and delivery settings"),
                    ("📦 Resources & Extensions", "resources", "Manage extensions, skills and packages"),
                    ("💰 Bedrock Pricing", "bedrock", "AWS Bedrock tier configuration"),
                    ("📋 View Configuration", "view", "View current settings"),
                    ("💾 Save & Exit", "save", "Save configuration and exit"),
                    ("❌ Exit Without Saving", "exit", "Exit without saving changes")
                ]
            },
            "model": {
                "title": "🤖 Pi-Ckl Model Settings",
                "description": "Configure AI provider and model settings",
                "items": [
                    ("Default Provider", "provider", f"Current: {self.config_manager.get_provider()}"),
                    ("Default Model", "model", f"Current: {self.config_manager.settings.get('model', {}).get('defaultModel', 'Not set')}"),
                    ("Thinking Level", "thinking", f"Current: {self.config_manager.get_thinking_level()}"),
                    ("Hide Thinking Block", "thinking_block", f"Current: {self.config_manager.settings.get('model', {}).get('hideThinkingBlock', False)}"),
                    ("Back to Main Menu", "main", "Return to main menu")
                ]
            },
            "ui": {
                "title": "🎨 Pi-Ckl UI Settings",
                "description": "Configure visual appearance and behavior",
                "items": [
                    ("Theme", "theme", f"Current: {self.config_manager.get_theme()}"),
                    ("Quiet Startup", "quiet", f"Current: {self.config_manager.settings.get('ui', {}).get('quietStartup', False)}"),
                    ("Project Trust", "trust", f"Current: {self.config_manager.settings.get('ui', {}).get('defaultProjectTrust', 'ask')}"),
                    ("Back to Main Menu", "main", "Return to main menu")
                ]
            },
            "system": {
                "title": "⚙️  Pi-Ckl System Settings",
                "description": "Configure system behavior and performance settings",
                "items": [
                    ("Compaction Settings", "compaction", "Configure message compaction"),
                    ("Retry Settings", "retry", "Configure retry behavior"),
                    ("Message Delivery", "delivery", "Configure message delivery"),
                    ("Back to Main Menu", "main", "Return to main menu")
                ]
            },
            "resources": {
                "title": "📦 Pi-Ckl Resources",
                "description": "Manage extensions, skills, and packages",
                "items": [
                    ("Packages", "packages", f"Current: {self.config_manager.settings.get('resources', {}).get('packages', [])}"),
                    ("Extensions", "extensions", f"Current: {self.config_manager.settings.get('resources', {}).get('extensions', [])}"),
                    ("Skills", "skills", f"Current: {self.config_manager.settings.get('resources', {}).get('skills', [])}"),
                    ("Back to Main Menu", "main", "Return to main menu")
                ]
            },
            "bedrock": {
                "title": "💰 Pi-Ckl Bedrock Settings",
                "description": "Configure AWS Bedrock pricing tier",
                "items": [
                    ("Default Tier", "tier", f"Current: {self.config_manager.get_bedrock_tier()}"),
                    ("Back to Main Menu", "main", "Return to main menu")
                ]
            }
        }
    
    def _clear_screen(self):
        """Clear the screen."""
        self.console.clear()
    
    def _show_header(self):
        """Show the header with title and description."""
        menu = self.menus[self.current_menu]
        header_text = f"{menu['title']}\n{menu['description']}"
        self.console.print(Panel.fit(header_text, style="bold cyan", border_style="bright_blue"))
    
    def _show_menu(self):
        """Show the current menu with selection."""
        menu_items = self.menus[self.current_menu]["items"]
        
        table = Table(show_header=False, box=ROUNDED, border_style="bright_blue")
        table.add_column("Option", style="bold green", no_wrap=True)
        table.add_column("Description", style="white")
        
        for i, (text, action, description) in enumerate(menu_items, 1):
            if i < 10:
                option = f" {i}. {text}"
            else:
                option = f"{i}. {text}"
            table.add_row(option, description)
        
        self.console.print(table)
    
    def _show_footer(self):
        """Show the footer with navigation help."""
        footer_text = "[bold]Navigation:[/bold] [cyan]↑↓[/cyan] arrows or [cyan]j/k[/cyan] to move, [cyan]Enter[/cyan] to select, [cyan]q[/cyan] to quit, [cyan]?[/cyan] for help"
        self.console.print(Panel.fit(footer_text, style="dim", border_style="dim"))
    
    def _show_help(self):
        """Show help screen."""
        help_text = """
[bold cyan]📖 Pi Configurator - Help[/bold cyan]

[bold]Navigation:[/bold]
  [cyan]↑↓[/cyan] arrows or [cyan]j/k[/cyan]  - Move selection up/down
  [cyan]Enter[/cyan] or [cyan]Space[/cyan]   - Select current item
  [cyan]q[/cyan] or [cyan]ESC[/cyan]         - Quit current menu
  [cyan]?[/cyan] or [cyan]F1[/cyan]          - Show this help

[bold]Editing:[/bold]
  Follow the prompts to edit values
  Changes are applied immediately
  Use 'Save & Exit' to persist changes

[bold]Main Menu Shortcuts:[/bold]
  [cyan]F10[/cyan]              - Save & Exit
  [cyan]F2[/cyan]               - Search settings

[dim]Press any key to continue...[/dim]
"""
        self._clear_screen()
        self.console.print(Panel.fit(help_text, style="white", border_style="bright_blue"))
        input("Press Enter to continue...")
    
    def _handle_action(self, action: str):
        """Handle menu actions."""
        if action == "main":
            self.current_menu = "main"
        
        elif action == "save":
            self.config_manager.save_settings()
            self.running = False
            self._clear_screen()
            self.console.print("[bold green]✅ Configuration saved successfully![/bold green]")
            self.console.print("[bold magenta]🎉 Thank you for using Pi-Ckl![/bold magenta]")
        
        elif action == "exit":
            self.running = False
            self._clear_screen()
            self.console.print("[bold red]❌ Exited without saving.[/bold red]")
        
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
        self.console.print("[bold cyan]🤖 Edit AI Provider[/bold cyan]")
        self.console.print(f"Current provider: [bold]{current}[/bold]\n")
        
        for i, provider in enumerate(providers, 1):
            marker = "▶" if provider == current else " "
            self.console.print(f"{marker} {i}. {provider}")
        
        choice = Prompt.ask("\nSelect provider (number or name)")
        
        if choice.isdigit() and 1 <= int(choice) <= len(providers):
            new_provider = providers[int(choice) - 1]
        elif choice in providers:
            new_provider = choice
        else:
            self.console.print("[bold red]❌ Invalid provider[/bold red]")
            input("Press Enter to continue...")
            return
        
        self.config_manager.settings.setdefault('model', {})['defaultProvider'] = new_provider
        self.console.print(f"[bold green]✅ Provider set to: {new_provider}[/bold green]")
        input("Press Enter to continue...")
        
        # Rebuild menus to update current values
        self.menus = self._build_menus()
    
    def _edit_bedrock_tier(self):
        """Edit Bedrock pricing tier."""
        tiers = ["flex", "standard", "spot"]
        current = self.config_manager.get_bedrock_tier()
        
        self._clear_screen()
        self.console.print("[bold cyan]💰 Edit Bedrock Pricing Tier[/bold cyan]")
        self.console.print(f"Current tier: [bold]{current}[/bold]\n")
        
        table = Table(show_header=False, box=ROUNDED)
        table.add_column("Option", style="bold")
        table.add_column("Description", style="white")
        
        table.add_row("▶ 1. flex", "Pay per request (recommended)")
        table.add_row("   2. standard", "Pay per vCPU-second")
        table.add_row("   3. spot", "Cheapest, but can be interrupted")
        
        self.console.print(table)
        
        choice = Prompt.ask("\nSelect tier (1-3 or name)")
        
        if choice == "1" or choice.lower() == "flex":
            new_tier = "flex"
        elif choice == "2" or choice.lower() == "standard":
            new_tier = "standard"
        elif choice == "3" or choice.lower() == "spot":
            new_tier = "spot"
        else:
            self.console.print("[bold red]❌ Invalid tier[/bold red]")
            input("Press Enter to continue...")
            return
        
        self.config_manager.settings.setdefault('bedrock', {})['defaultTier'] = new_tier
        self.console.print(f"[bold green]✅ Bedrock tier set to: {new_tier}[/bold green]")
        
        if new_tier == "flex":
            self.console.print("[bold yellow]💡 Tip:[/bold yellow] 'flex' tier is pay-per-request, recommended for variable workloads")
        elif new_tier == "standard":
            self.console.print("[bold yellow]💡 Tip:[/bold yellow] 'standard' tier is pay-per-vCPU-second, for consistent workloads")
        else:
            self.console.print("[bold yellow]💡 Tip:[/bold yellow] 'spot' tier is cheapest but instances can be interrupted")
        
        input("Press Enter to continue...")
        
        # Rebuild menus to update current values
        self.menus = self._build_menus()
    
    def _edit_theme(self):
        """Edit theme setting."""
        themes = ["dark", "light", "system"]
        current = self.config_manager.get_theme()
        
        self._clear_screen()
        self.console.print("[bold cyan]🎨 Edit Theme[/bold cyan]")
        self.console.print(f"Current theme: [bold]{current}[/bold]\n")
        
        for i, theme in enumerate(themes, 1):
            marker = "▶" if theme == current else " "
            self.console.print(f"{marker} {i}. {theme}")
        
        choice = Prompt.ask("\nSelect theme (1-3 or name)")
        
        if choice.isdigit() and 1 <= int(choice) <= len(themes):
            new_theme = themes[int(choice) - 1]
        elif choice in themes:
            new_theme = choice
        else:
            self.console.print("[bold red]❌ Invalid theme[/bold red]")
            input("Press Enter to continue...")
            return
        
        self.config_manager.settings.setdefault('ui', {})['theme'] = new_theme
        self.console.print(f"[bold green]✅ Theme set to: {new_theme}[/bold green]")
        input("Press Enter to continue...")
        
        # Rebuild menus to update current values
        self.menus = self._build_menus()
    
    def run(self) -> None:
        """Run the modern TUI."""
        try:
            while self.running:
                self._clear_screen()
                self._show_header()
                self._show_menu()
                self._show_footer()
                
                # Get user choice
                menu_items = self.menus[self.current_menu]["items"]
                choice = Prompt.ask("\nSelect option (1-{})".format(len(menu_items)))
                
                # Handle special commands
                if choice.lower() in ['q', 'quit', 'exit']:
                    if self.current_menu == "main":
                        self.running = False
                    else:
                        self.current_menu = "main"
                        continue
                
                elif choice.lower() in ['?', 'help']:
                    self._show_help()
                    continue
                
                # Handle numeric selection
                elif choice.isdigit():
                    selection = int(choice) - 1
                    if 0 <= selection < len(menu_items):
                        text, action, description = menu_items[selection]
                        self._handle_action(action)
                        continue
                
                self.console.print("[bold red]❌ Invalid option. Please try again.[/bold red]")
                input("Press Enter to continue...")
            
        except KeyboardInterrupt:
            self._clear_screen()
            self.console.print("[bold red]❌ Operation cancelled by user.[/bold red]")
        except Exception as e:
            self._clear_screen()
            self.console.print(f"[bold red]❌ Error: {e}[/bold red]")
        finally:
            self.console.print("[bold magenta]👋 Thank you for using Pi-Ckl![/bold magenta]")

class ModernTUIHandler:
    """Handler for modern TUI operations."""
    
    def __init__(self, config_manager: ConfigManager):
        self.config_manager = config_manager
    
    def run(self) -> None:
        """Run the modern TUI."""
        try:
            tui = ModernTUI(self.config_manager)
            tui.run()
        except ImportError as e:
            print(f"Modern TUI requires Rich library: {e}")
            print("Falling back to simple TUI...")
            from pi_configurator.tui.simple_tui_handler import SimpleTUIHandler
            simple_tui = SimpleTUIHandler(self.config_manager)
            simple_tui.run()
        except Exception as e:
            print(f"Modern TUI failed: {e}")
            print("Falling back to simple TUI...")
            from pi_configurator.tui.simple_tui_handler import SimpleTUIHandler
            simple_tui = SimpleTUIHandler(self.config_manager)
            simple_tui.run()
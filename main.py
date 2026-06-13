"""
Pi Coding Agent Configuration Tool - Main Entry Point

This is the main entry point that orchestrates the modular components.
"""

import sys
import os
import argparse

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import modular components from the new package structure
from pi_configurator.core.config_manager import ConfigManager
from pi_configurator.tui.interactive_handler import InteractiveHandler
from pi_configurator.tui.tui_handler import TUIHandler
from pi_configurator.tui.simple_tui_handler import SimpleTUIHandler
from pi_configurator.tui.readline_tui import ReadlineTUIHandler
from pi_configurator.tui.keyboard_tui import KeyboardTUIHandler

__version__ = "1.0.0"
__author__ = "Pi-Ckl Team"
__license__ = "MIT"

def main():
    """Main entry point for the application."""
    try:
        # Check dependencies
        from pi_configurator.utils.dependencies import DependencyManager
        DependencyManager.check_and_warn()
        parser = argparse.ArgumentParser(
            description="Pi-Ckl - Configuration Tool for Pi Coding Agent",
            formatter_class=argparse.RawDescriptionHelpFormatter
        )
        
        # Add arguments
        parser.add_argument("-i", "--interactive", action="store_true",
                           help="Run interactive menu-driven configuration")
        parser.add_argument("-t", "--tui", action="store_true",
                           help="Run advanced terminal UI (like make menuconfig)")
        parser.add_argument("-c", "--config-dir", type=str,
                           help="Override config directory (default: ~/.pi/agent)")
        parser.add_argument("--list", action="store_true",
                           help="List all available settings and their values")
        parser.add_argument("--default-bedrock-tier", type=str,
                           help="AWS Bedrock pricing tier: flex, standard, spot")
        parser.add_argument("--list-models", action="store_true",
                           help="List all available models for the current provider")
        parser.add_argument("--version", action="version",
                           version=f"Pi-Ckl v{__version__}",
                           help="Show version information and exit")
        
        args = parser.parse_args()
        
        # Initialize config manager
        config_manager = ConfigManager(args.config_dir)
        
        # Handle --list option
        if args.list:
            config_manager.list_settings()
            return
        
        # Handle --list-models option
        if args.list_models:
            config_manager.list_available_models()
            return
        
        # Handle --default-bedrock-tier option
        if args.default_bedrock_tier:
            config_manager.set_bedrock_tier(args.default_bedrock_tier)
            return
        
        # Handle additional CLI arguments (for future expansion)
        # These would be parsed from sys.argv if needed
        # For now, the Makefile targets use direct configurator.sh calls
        
        # Handle TUI mode (advanced terminal UI)
        if args.tui:
            try:
                tui_handler = TUIHandler(config_manager)
                tui_handler.run()
            except Exception as e:
                print(f"Advanced TUI mode failed: {e}")
                print("Falling back to simple TUI mode...")
                simple_tui_handler = SimpleTUIHandler(config_manager)
                simple_tui_handler.run()
            return
        
        # Handle interactive mode (use keyboard TUI by default)
        if args.interactive:
            try:
                keyboard_tui_handler = KeyboardTUIHandler(config_manager)
                keyboard_tui_handler.run()
            except Exception as e:
                print(f"Keyboard TUI mode failed: {e}")
                print("Falling back to readline TUI mode...")
                try:
                    readline_tui_handler = ReadlineTUIHandler(config_manager)
                    readline_tui_handler.run()
                except Exception as e2:
                    print(f"Readline TUI mode failed: {e2}")
                    print("Falling back to simple TUI mode...")
                    simple_tui_handler = SimpleTUIHandler(config_manager)
                    simple_tui_handler.run()
            return
        
        # Print help if no arguments provided
        if len(sys.argv) == 1:
            parser.print_help()
            sys.exit(1)
            
    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user.")
        sys.exit(130)
    except Exception as e:
        print(f"\nError: {e}")
        print("For help, use: python3 main.py --help")
        sys.exit(1)

if __name__ == "__main__":
    main()
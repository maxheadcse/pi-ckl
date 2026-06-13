"""
Interactive Handler

Handles interactive menu-driven configuration for the Pi Coding Agent Configuration Tool.
"""

import sys
from typing import Dict, Any
from pi_configurator.core.config_manager import ConfigManager

class InteractiveHandler:
    """Handles interactive menu-driven configuration."""
    
    def __init__(self, config_manager: ConfigManager):
        """Initialize the interactive handler.
        
        Args:
            config_manager: ConfigManager instance
        """
        self.config_manager = config_manager
    
    def run(self) -> None:
        """Run the interactive menu-driven configuration."""
        while True:
            print("\n" + "="*60)
            print("Pi Coding Agent Configuration - Interactive Mode")
            print("="*60)
            print("1. Model & Thinking Options")
            print("2. UI & Display Settings")
            print("3. Compaction Settings")
            print("4. Retry Settings")
            print("5. Message Delivery")
            print("6. Terminal & Images")
            print("7. Shell Configuration")
            print("8. Sessions")
            print("9. Markdown")
            print("10. Resources")
            print("11. Bedrock Pricing Tier")
            print("12. List Available Models")
            print("13. View Current Configuration")
            print("14. Save and Exit")
            print("0. Exit without saving")
            print("="*60)
            
            choice = input("Select an option (0-14): ").strip()
            
            if choice == "0":
                print("Exiting without saving.")
                break
            
            elif choice == "1":
                self.model_menu()
            elif choice == "2":
                self.ui_menu()
            elif choice == "3":
                self.compaction_menu()
            elif choice == "4":
                self.retry_menu()
            elif choice == "5":
                self.message_delivery_menu()
            elif choice == "6":
                self.terminal_menu()
            elif choice == "7":
                self.shell_menu()
            elif choice == "8":
                self.sessions_menu()
            elif choice == "9":
                self.markdown_menu()
            elif choice == "10":
                self.resources_menu()
            elif choice == "11":
                self.bedrock_menu()
            elif choice == "12":
                self.config_manager.list_available_models()
                input("\nPress Enter to continue...")
            elif choice == "13":
                self.config_manager.list_settings()
                input("\nPress Enter to continue...")
            elif choice == "14":
                self.config_manager.save_settings(self.config_manager.settings)
                print("Configuration saved to ~/.pi/agent/settings.json")
                break
            else:
                print("Invalid option. Please try again.")
    
    def model_menu(self) -> None:
        """Menu for model and thinking settings."""
        print("\nModel & Thinking Options:")
        print(f"1. Default Provider: {self.config_manager.get_provider()}")
        print(f"2. Default Model: {self.config_manager.settings.get('model', {}).get('defaultModel', '')}")
        print(f"3. Default Thinking Level: {self.config_manager.get_thinking_level()}")
        print(f"4. Hide Thinking Block: {self.config_manager.settings.get('model', {}).get('hideThinkingBlock', False)}")
        print("5. Back to main menu")
        
        choice = input("Select option: ").strip()
        
        if choice == "1":
            providers = ["anthropic", "openai", "google", "aws-bedrock"]
            print(f"Available providers: {', '.join(providers)}")
            provider = input("Enter provider name: ").strip()
            if provider in providers:
                self.config_manager.settings.setdefault('model', {})['defaultProvider'] = provider
                print(f"Default provider set to: {provider}")
            else:
                print(f"Invalid provider: {provider}")
        
        elif choice == "2":
            provider = self.config_manager.get_provider()
            if provider == "anthropic":
                models = [
                    "claude-3-5-sonnet-20240620",
                    "claude-3-opus-20240229",
                    "claude-3-haiku-20240307",
                    "claude-2.1",
                    "claude-2.0"
                ]
            elif provider == "openai":
                models = [
                    "gpt-4-turbo",
                    "gpt-4",
                    "gpt-3.5-turbo",
                    "gpt-4o"
                ]
            elif provider == "google":
                models = [
                    "gemini-pro",
                    "gemini-pro-vision",
                    "chat-bison"
                ]
            elif provider == "aws-bedrock":
                models = [
                    "anthropic.claude-3-5-sonnet-20240620-v1:0",
                    "anthropic.claude-3-opus-20240229-v1:0",
                    "anthropic.claude-3-haiku-20240307-v1:0",
                    "amazon.titan-text-express-v1",
                    "meta.llama3-70b-instruct-v1:0",
                    "meta.llama3-8b-instruct-v1:0",
                    "cohere.command-r-v1:0",
                    "cohere.command-r-plus-v1:0"
                ]
            else:
                models = ["Specify model name"]
            
            print(f"Available models for {provider}:\n")
            for i, model in enumerate(models, 1):
                print(f"  {i}. {model}")
            
            model_input = input("Enter model name (or number): ").strip()
            if model_input.isdigit() and 1 <= int(model_input) <= len(models):
                self.config_manager.settings.setdefault('model', {})['defaultModel'] = models[int(model_input) - 1]
            else:
                self.config_manager.settings.setdefault('model', {})['defaultModel'] = model_input
            
            print(f"Default model set to: {self.config_manager.settings['model']['defaultModel']}")
        
        elif choice == "3":
            levels = ["off", "minimal", "low", "medium", "high", "xhigh"]
            print(f"Available levels: {', '.join(levels)}")
            level = input("Enter thinking level: ").strip()
            if level in levels:
                self.config_manager.settings.setdefault('model', {})['defaultThinkingLevel'] = level
                print(f"Default thinking level set to: {level}")
            else:
                print(f"Invalid level: {level}")
        
        elif choice == "4":
            current = self.config_manager.settings.get('model', {}).get('hideThinkingBlock', False)
            new_val = not current
            self.config_manager.settings.setdefault('model', {})['hideThinkingBlock'] = new_val
            print(f"Hide thinking block set to: {new_val}")
        
        elif choice == "5":
            return
        
        input("Press Enter to continue...")
    
    def ui_menu(self) -> None:
        """Menu for UI and display settings."""
        print("\nUI & Display Settings:")
        print(f"1. Theme: {self.config_manager.get_theme()}")
        print(f"2. Quiet Startup: {self.config_manager.settings.get('ui', {}).get('quietStartup', False)}")
        print(f"3. Default Project Trust: {self.config_manager.settings.get('ui', {}).get('defaultProjectTrust', 'ask')}")
        print(f"4. Collapse Changelog: {self.config_manager.settings.get('ui', {}).get('collapseChangelog', False)}")
        print(f"5. Enable Install Telemetry: {self.config_manager.settings.get('ui', {}).get('enableInstallTelemetry', True)}")
        print(f"6. Double Escape Action: {self.config_manager.settings.get('ui', {}).get('doubleEscapeAction', 'tree')}")
        print(f"7. Tree Filter Mode: {self.config_manager.settings.get('ui', {}).get('treeFilterMode', 'default')}")
        print(f"8. Editor Padding X: {self.config_manager.settings.get('ui', {}).get('editorPaddingX', 0)}")
        print(f"9. Autocomplete Max Visible: {self.config_manager.settings.get('ui', {}).get('autocompleteMaxVisible', 5)}")
        print(f"10. Show Hardware Cursor: {self.config_manager.settings.get('ui', {}).get('showHardwareCursor', False)}")
        print("11. Back to main menu")
        
        choice = input("Select option: ").strip()
        
        if choice == "1":
            themes = ["dark", "light", "system"]
            print(f"Available themes: {', '.join(themes)}")
            theme = input("Enter theme name: ").strip()
            if theme in themes:
                self.config_manager.settings.setdefault('ui', {})['theme'] = theme
                print(f"Theme set to: {theme}")
            else:
                print(f"Invalid theme: {theme}")
        
        elif choice == "2":
            current = self.config_manager.settings.get('ui', {}).get('quietStartup', False)
            new_val = not current
            self.config_manager.settings.setdefault('ui', {})['quietStartup'] = new_val
            print(f"Quiet startup set to: {new_val}")
        
        elif choice == "3":
            trust_options = ["ask", "always", "never"]
            print(f"Available options: {', '.join(trust_options)}")
            trust = input("Enter trust option: ").strip()
            if trust in trust_options:
                self.config_manager.settings.setdefault('ui', {})['defaultProjectTrust'] = trust
                print(f"Default project trust set to: {trust}")
            else:
                print(f"Invalid option: {trust}")
        
        elif choice == "4":
            current = self.config_manager.settings.get('ui', {}).get('collapseChangelog', False)
            new_val = not current
            self.config_manager.settings.setdefault('ui', {})['collapseChangelog'] = new_val
            print(f"Collapse changelog set to: {new_val}")
        
        elif choice == "5":
            current = self.config_manager.settings.get('ui', {}).get('enableInstallTelemetry', True)
            new_val = not current
            self.config_manager.settings.setdefault('ui', {})['enableInstallTelemetry'] = new_val
            print(f"Install telemetry set to: {new_val}")
        
        elif choice == "6":
            actions = ["tree", "fork", "none"]
            print(f"Available actions: {', '.join(actions)}")
            action = input("Enter action: ").strip()
            if action in actions:
                self.config_manager.settings.setdefault('ui', {})['doubleEscapeAction'] = action
                print(f"Double escape action set to: {action}")
            else:
                print(f"Invalid action: {action}")
        
        elif choice == "7":
            modes = ["default", "exact", "fuzzy"]
            print(f"Available modes: {', '.join(modes)}")
            mode = input("Enter mode: ").strip()
            if mode in modes:
                self.config_manager.settings.setdefault('ui', {})['treeFilterMode'] = mode
                print(f"Tree filter mode set to: {mode}")
            else:
                print(f"Invalid mode: {mode}")
        
        elif choice == "8":
            padding = input("Enter editor padding (0-100): ").strip()
            if padding.isdigit() and 0 <= int(padding) <= 100:
                self.config_manager.settings.setdefault('ui', {})['editorPaddingX'] = int(padding)
                print(f"Editor padding X set to: {padding}")
            else:
                print("Invalid value, must be 0-100")
        
        elif choice == "9":
            max_visible = input("Enter max autocomplete visible (1-20): ").strip()
            if max_visible.isdigit() and 1 <= int(max_visible) <= 20:
                self.config_manager.settings.setdefault('ui', {})['autocompleteMaxVisible'] = int(max_visible)
                print(f"Max autocomplete visible set to: {max_visible}")
            else:
                print("Invalid value, must be 1-20")
        
        elif choice == "10":
            current = self.config_manager.settings.get('ui', {}).get('showHardwareCursor', False)
            new_val = not current
            self.config_manager.settings.setdefault('ui', {})['showHardwareCursor'] = new_val
            print(f"Show hardware cursor set to: {new_val}")
        
        elif choice == "11":
            return
        
        input("Press Enter to continue...")
    
    def compaction_menu(self) -> None:
        """Menu for compaction settings."""
        print("\nCompaction Settings:")
        print(f"1. Enabled: {self.config_manager.settings.get('compaction', {}).get('enabled', True)}")
        print(f"2. Reserve Tokens: {self.config_manager.settings.get('compaction', {}).get('reserveTokens', 16384)}")
        print(f"3. Keep Recent Tokens: {self.config_manager.settings.get('compaction', {}).get('keepRecentTokens', 20000)}")
        print("4. Back to main menu")
        
        choice = input("Select option: ").strip()
        
        if choice == "1":
            current = self.config_manager.settings.get('compaction', {}).get('enabled', True)
            new_val = not current
            self.config_manager.settings.setdefault('compaction', {})['enabled'] = new_val
            print(f"Compaction enabled set to: {new_val}")
        
        elif choice == "2":
            tokens = input("Enter reserve tokens (0-50000): ").strip()
            if tokens.isdigit() and 0 <= int(tokens) <= 50000:
                self.config_manager.settings.setdefault('compaction', {})['reserveTokens'] = int(tokens)
                print(f"Reserve tokens set to: {tokens}")
            else:
                print("Invalid value, must be 0-50000")
        
        elif choice == "3":
            tokens = input("Enter keep recent tokens (0-50000): ").strip()
            if tokens.isdigit() and 0 <= int(tokens) <= 50000:
                self.config_manager.settings.setdefault('compaction', {})['keepRecentTokens'] = int(tokens)
                print(f"Keep recent tokens set to: {tokens}")
            else:
                print("Invalid value, must be 0-50000")
        
        elif choice == "4":
            return
        
        input("Press Enter to continue...")
    
    def retry_menu(self) -> None:
        """Menu for retry settings."""
        print("\nRetry Settings:")
        print(f"1. Enabled: {self.config_manager.settings.get('retry', {}).get('enabled', True)}")
        print(f"2. Max Retries: {self.config_manager.settings.get('retry', {}).get('maxRetries', 3)}")
        print(f"3. Base Delay (ms): {self.config_manager.settings.get('retry', {}).get('baseDelayMs', 2000)}")
        print("4. Back to main menu")
        
        choice = input("Select option: ").strip()
        
        if choice == "1":
            current = self.config_manager.settings.get('retry', {}).get('enabled', True)
            new_val = not current
            self.config_manager.settings.setdefault('retry', {})['enabled'] = new_val
            print(f"Retry enabled set to: {new_val}")
        
        elif choice == "2":
            retries = input("Enter max retries (0-10): ").strip()
            if retries.isdigit() and 0 <= int(retries) <= 10:
                self.config_manager.settings.setdefault('retry', {})['maxRetries'] = int(retries)
                print(f"Max retries set to: {retries}")
            else:
                print("Invalid value, must be 0-10")
        
        elif choice == "3":
            delay = input("Enter base delay in ms (100-10000): ").strip()
            if delay.isdigit() and 100 <= int(delay) <= 10000:
                self.config_manager.settings.setdefault('retry', {})['baseDelayMs'] = int(delay)
                print(f"Base delay set to: {delay}ms")
            else:
                print("Invalid value, must be 100-10000")
        
        elif choice == "4":
            return
        
        input("Press Enter to continue...")
    
    def message_delivery_menu(self) -> None:
        """Menu for message delivery settings."""
        print("\nMessage Delivery Settings:")
        print(f"1. Steering Mode: {self.config_manager.settings.get('messageDelivery', {}).get('steeringMode', 'one-at-a-time')}")
        print(f"2. Follow-up Mode: {self.config_manager.settings.get('messageDelivery', {}).get('followUpMode', 'one-at-a-time')}")
        print(f"3. Transport: {self.config_manager.settings.get('messageDelivery', {}).get('transport', 'auto')}")
        print(f"4. HTTP Idle Timeout (ms): {self.config_manager.settings.get('messageDelivery', {}).get('httpIdleTimeoutMs', 300000)}")
        print(f"5. WebSocket Connect Timeout (ms): {self.config_manager.settings.get('messageDelivery', {}).get('websocketConnectTimeoutMs', 15000)}")
        print("6. Back to main menu")
        
        choice = input("Select option: ").strip()
        
        if choice == "1":
            modes = ["one-at-a-time", "batch", "stream"]
            print(f"Available modes: {', '.join(modes)}")
            mode = input("Enter steering mode: ").strip()
            if mode in modes:
                self.config_manager.settings.setdefault('messageDelivery', {})['steeringMode'] = mode
                print(f"Steering mode set to: {mode}")
            else:
                print(f"Invalid mode: {mode}")
        
        elif choice == "2":
            modes = ["one-at-a-time", "batch", "stream"]
            print(f"Available modes: {', '.join(modes)}")
            mode = input("Enter follow-up mode: ").strip()
            if mode in modes:
                self.config_manager.settings.setdefault('messageDelivery', {})['followUpMode'] = mode
                print(f"Follow-up mode set to: {mode}")
            else:
                print(f"Invalid mode: {mode}")
        
        elif choice == "3":
            transports = ["auto", "sse", "websocket", "websocket-cached"]
            print(f"Available transports: {', '.join(transports)}")
            transport = input("Enter transport: ").strip()
            if transport in transports:
                self.config_manager.settings.setdefault('messageDelivery', {})['transport'] = transport
                print(f"Transport set to: {transport}")
            else:
                print(f"Invalid transport: {transport}")
        
        elif choice == "4":
            timeout = input("Enter HTTP idle timeout in ms (0-1000000): ").strip()
            if timeout.isdigit() and 0 <= int(timeout) <= 1000000:
                self.config_manager.settings.setdefault('messageDelivery', {})['httpIdleTimeoutMs'] = int(timeout)
                print(f"HTTP idle timeout set to: {timeout}ms")
            else:
                print("Invalid value, must be 0-1000000")
        
        elif choice == "5":
            timeout = input("Enter WebSocket connect timeout in ms (0-100000): ").strip()
            if timeout.isdigit() and 0 <= int(timeout) <= 100000:
                self.config_manager.settings.setdefault('messageDelivery', {})['websocketConnectTimeoutMs'] = int(timeout)
                print(f"WebSocket connect timeout set to: {timeout}ms")
            else:
                print("Invalid value, must be 0-100000")
        
        elif choice == "6":
            return
        
        input("Press Enter to continue...")
    
    def terminal_menu(self) -> None:
        """Menu for terminal and images settings."""
        print("\nTerminal & Images Settings:")
        print(f"1. Show Images: {self.config_manager.settings.get('terminal', {}).get('showImages', True)}")
        print(f"2. Image Width Cells: {self.config_manager.settings.get('terminal', {}).get('imageWidthCells', 60)}")
        print(f"3. Clear On Shrink: {self.config_manager.settings.get('terminal', {}).get('clearOnShrink', False)}")
        print(f"4. Auto Resize Images: {self.config_manager.settings.get('images', {}).get('autoResize', True)}")
        print(f"5. Block Images: {self.config_manager.settings.get('images', {}).get('blockImages', False)}")
        print("6. Back to main menu")
        
        choice = input("Select option: ").strip()
        
        if choice == "1":
            current = self.config_manager.settings.get('terminal', {}).get('showImages', True)
            new_val = not current
            self.config_manager.settings.setdefault('terminal', {})['showImages'] = new_val
            print(f"Show images set to: {new_val}")
        
        elif choice == "2":
            width = input("Enter image width in cells (10-100): ").strip()
            if width.isdigit() and 10 <= int(width) <= 100:
                self.config_manager.settings.setdefault('terminal', {})['imageWidthCells'] = int(width)
                print(f"Image width set to: {width} cells")
            else:
                print("Invalid value, must be 10-100")
        
        elif choice == "3":
            current = self.config_manager.settings.get('terminal', {}).get('clearOnShrink', False)
            new_val = not current
            self.config_manager.settings.setdefault('terminal', {})['clearOnShrink'] = new_val
            print(f"Clear on shrink set to: {new_val}")
        
        elif choice == "4":
            current = self.config_manager.settings.get('images', {}).get('autoResize', True)
            new_val = not current
            self.config_manager.settings.setdefault('images', {})['autoResize'] = new_val
            print(f"Auto resize images set to: {new_val}")
        
        elif choice == "5":
            current = self.config_manager.settings.get('images', {}).get('blockImages', False)
            new_val = not current
            self.config_manager.settings.setdefault('images', {})['blockImages'] = new_val
            print(f"Block images set to: {new_val}")
        
        elif choice == "6":
            return
        
        input("Press Enter to continue...")
    
    def shell_menu(self) -> None:
        """Menu for shell settings."""
        print("\nShell Configuration:")
        print(f"1. Shell Path: {self.config_manager.settings.get('shell', {}).get('shellPath', '')}")
        print(f"2. Shell Command Prefix: {self.config_manager.settings.get('shell', {}).get('shellCommandPrefix', '')}")
        print(f"3. NPM Command: {self.config_manager.settings.get('shell', {}).get('npmCommand', [])}")
        print("4. Back to main menu")
        
        choice = input("Select option: ").strip()
        
        if choice == "1":
            path = input("Enter shell path (leave empty for default): ").strip()
            self.config_manager.settings.setdefault('shell', {})['shellPath'] = path if path else ""
            print(f"Shell path set to: {path if path else 'default'}")
        
        elif choice == "2":
            prefix = input("Enter shell command prefix (leave empty for none): ").strip()
            self.config_manager.settings.setdefault('shell', {})['shellCommandPrefix'] = prefix if prefix else ""
            print(f"Shell command prefix set to: {prefix if prefix else 'none'}")
        
        elif choice == "3":
            print("Enter npm command as space-separated arguments (e.g., 'install -g package'):")
            cmd = input().strip()
            if cmd:
                self.config_manager.settings.setdefault('shell', {})['npmCommand'] = cmd.split()
            else:
                self.config_manager.settings.setdefault('shell', {})['npmCommand'] = []
            print(f"NPM command set to: {self.config_manager.settings['shell']['npmCommand']}")
        
        elif choice == "4":
            return
        
        input("Press Enter to continue...")
    
    def sessions_menu(self) -> None:
        """Menu for sessions settings."""
        print("\nSessions Settings:")
        print(f"1. Session Directory: {self.config_manager.settings.get('sessions', {}).get('sessionDir', '')}")
        print("2. Back to main menu")
        
        choice = input("Select option: ").strip()
        
        if choice == "1":
            path = input("Enter session directory path (leave empty for default): ").strip()
            self.config_manager.settings.setdefault('sessions', {})['sessionDir'] = path if path else ""
            print(f"Session directory set to: {path if path else 'default'}")
        
        elif choice == "2":
            return
        
        input("Press Enter to continue...")
    
    def markdown_menu(self) -> None:
        """Menu for markdown settings."""
        print("\nMarkdown Settings:")
        print(f"1. Code Block Indent: {self.config_manager.settings.get('markdown', {}).get('codeBlockIndent', '  ')}")
        print("2. Back to main menu")
        
        choice = input("Select option: ").strip()
        
        if choice == "1":
            indent = input("Enter code block indent (e.g., '    ' or '  '): ").strip()
            self.config_manager.settings.setdefault('markdown', {})['codeBlockIndent'] = indent
            print(f"Code block indent set to: '{indent}'")
        
        elif choice == "2":
            return
        
        input("Press Enter to continue...")
    
    def resources_menu(self) -> None:
        """Menu for resources settings."""
        print("\nResources Settings:")
        print(f"1. Packages: {self.config_manager.settings.get('resources', {}).get('packages', [])}")
        print(f"2. Extensions: {self.config_manager.settings.get('resources', {}).get('extensions', [])}")
        print(f"3. Skills: {self.config_manager.settings.get('resources', {}).get('skills', [])}")
        print(f"4. Prompts: {self.config_manager.settings.get('resources', {}).get('prompts', [])}")
        print(f"5. Themes: {self.config_manager.settings.get('resources', {}).get('themes', [])}")
        print(f"6. Enable Skill Commands: {self.config_manager.settings.get('resources', {}).get('enableSkillCommands', True)}")
        print("7. Back to main menu")
        
        choice = input("Select option: ").strip()
        
        if choice == "1":
            packages = input("Enter packages as space-separated values: ").strip()
            self.config_manager.settings.setdefault('resources', {})['packages'] = packages.split() if packages else []
            print(f"Packages set to: {self.config_manager.settings['resources']['packages']}")
        
        elif choice == "2":
            extensions = input("Enter extensions as space-separated values: ").strip()
            self.config_manager.settings.setdefault('resources', {})['extensions'] = extensions.split() if extensions else []
            print(f"Extensions set to: {self.config_manager.settings['resources']['extensions']}")
        
        elif choice == "3":
            skills = input("Enter skills as space-separated values: ").strip()
            self.config_manager.settings.setdefault('resources', {})['skills'] = skills.split() if skills else []
            print(f"Skills set to: {self.config_manager.settings['resources']['skills']}")
        
        elif choice == "4":
            prompts = input("Enter prompts as space-separated values: ").strip()
            self.config_manager.settings.setdefault('resources', {})['prompts'] = prompts.split() if prompts else []
            print(f"Prompts set to: {self.config_manager.settings['resources']['prompts']}")
        
        elif choice == "5":
            themes = input("Enter themes as space-separated values: ").strip()
            self.config_manager.settings.setdefault('resources', {})['themes'] = themes.split() if themes else []
            print(f"Themes set to: {self.config_manager.settings['resources']['themes']}")
        
        elif choice == "6":
            current = self.config_manager.settings.get('resources', {}).get('enableSkillCommands', True)
            new_val = not current
            self.config_manager.settings.setdefault('resources', {})['enableSkillCommands'] = new_val
            print(f"Enable skill commands set to: {new_val}")
        
        elif choice == "7":
            return
        
        input("Press Enter to continue...")
    
    def bedrock_menu(self) -> None:
        """Menu for Bedrock pricing tier settings."""
        print("\nBedrock Pricing Tier:")
        print(f"1. Default Tier: {self.config_manager.get_bedrock_tier()}")
        print("2. Back to main menu")
        
        choice = input("Select option: ").strip()
        
        if choice == "1":
            tiers = ["flex", "standard", "spot"]
            print(f"Available tiers: {', '.join(tiers)}")
            tier = input("Enter tier (flex, standard, spot): ").strip()
            if tier in tiers:
                self.config_manager.settings.setdefault('bedrock', {})['defaultTier'] = tier
                print(f"Bedrock tier set to: {tier}")
                
                # Provide additional guidance
                if tier == "flex":
                    print("Tip: 'flex' tier is pay-per-request and recommended for variable workloads")
                elif tier == "standard":
                    print("Tip: 'standard' tier is pay-per-vCPU-second and recommended for consistent workloads")
                elif tier == "spot":
                    print("Tip: 'spot' tier is cheapest but instances can be interrupted")
            else:
                print(f"Invalid tier: {tier}")
        
        elif choice == "2":
            return
        
        input("Press Enter to continue...")
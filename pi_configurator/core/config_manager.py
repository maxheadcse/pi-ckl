"""
Core Configuration Manager

Handles configuration loading, saving, and basic operations with JSON storage.
"""

import os
import json
from typing import Dict, Any, List
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ConfigManager:
    """Core configuration manager with JSON storage."""
    
    def __init__(self, config_dir: str = None):
        """Initialize the config manager.
        
        Args:
            config_dir: Directory for config files (default: ~/.pi/agent)
        """
        self.config_dir = config_dir or os.path.expanduser("~/.pi/agent")
        self.settings_file = os.path.join(self.config_dir, "settings.json")
        
        # Create config directory if it doesn't exist
        os.makedirs(self.config_dir, exist_ok=True)
        
        # Load settings
        self.settings = self.load_settings()
    
    def load_settings(self) -> Dict[str, Any]:
        """Load settings from JSON file."""
        if os.path.exists(self.settings_file):
            try:
                with open(self.settings_file, 'r') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                logger.error(f"Invalid JSON in {self.settings_file}, creating new file.")
                return self.get_default_settings()
            except Exception as e:
                logger.error(f"Error loading settings: {e}")
                return self.get_default_settings()
        else:
            # Create default settings file
            default_settings = self.get_default_settings()
            self.save_settings(default_settings)
            return default_settings
    
    def get_default_settings(self) -> Dict[str, Any]:
        """Return default configuration schema."""
        return {
            "model": {
                "defaultProvider": "anthropic",
                "defaultModel": "claude-3-5-sonnet-20240620",
                "defaultThinkingLevel": "medium",
                "hideThinkingBlock": False,
                "enabledModels": []
            },
            "ui": {
                "theme": "dark",
                "quietStartup": False,
                "defaultProjectTrust": "ask",
                "collapseChangelog": False,
                "enableInstallTelemetry": True,
                "doubleEscapeAction": "tree",
                "treeFilterMode": "default",
                "editorPaddingX": 0,
                "autocompleteMaxVisible": 5,
                "showHardwareCursor": False
            },
            "compaction": {
                "enabled": True,
                "reserveTokens": 16384,
                "keepRecentTokens": 20000
            },
            "retry": {
                "enabled": True,
                "maxRetries": 3,
                "baseDelayMs": 2000
            },
            "messageDelivery": {
                "steeringMode": "one-at-a-time",
                "followUpMode": "one-at-a-time",
                "transport": "auto",
                "httpIdleTimeoutMs": 300000,
                "websocketConnectTimeoutMs": 15000
            },
            "terminal": {
                "showImages": True,
                "imageWidthCells": 60,
                "clearOnShrink": False
            },
            "images": {
                "autoResize": True,
                "blockImages": False
            },
            "shell": {
                "shellPath": "",
                "shellCommandPrefix": "",
                "npmCommand": []
            },
            "sessions": {
                "sessionDir": ""
            },
            "markdown": {
                "codeBlockIndent": "  "
            },
            "resources": {
                "packages": [],
                "extensions": [],
                "skills": [],
                "prompts": [],
                "themes": [],
                "enableSkillCommands": True
            },
            "bedrock": {
                "defaultTier": "flex"
            }
        }
    
    def save_settings(self, settings: Dict[str, Any] = None) -> None:
        """Save settings to JSON file."""
        if settings is None:
            settings = self.settings
        
        try:
            with open(self.settings_file, 'w') as f:
                json.dump(settings, f, indent=2)
            logger.info(f"Settings saved to {self.settings_file}")
        except Exception as e:
            logger.error(f"Error saving settings: {e}")
            raise
    
    def list_settings(self) -> None:
        """List all available settings and their current values."""
        print("Available Settings:\n")
        
        # Group settings by category
        categories = {
            "Model & Thinking": [
                "model.defaultProvider", "model.defaultModel", "model.defaultThinkingLevel", 
                "model.hideThinkingBlock", "model.enabledModels"
            ],
            "UI & Display": [
                "ui.theme", "ui.quietStartup", "ui.defaultProjectTrust", "ui.collapseChangelog", 
                "ui.enableInstallTelemetry", "ui.doubleEscapeAction", "ui.treeFilterMode", 
                "ui.editorPaddingX", "ui.autocompleteMaxVisible", "ui.showHardwareCursor"
            ],
            "Compaction": [
                "compaction.enabled", "compaction.reserveTokens", "compaction.keepRecentTokens"
            ],
            "Retry": [
                "retry.enabled", "retry.maxRetries", "retry.baseDelayMs"
            ],
            "Message Delivery": [
                "messageDelivery.steeringMode", "messageDelivery.followUpMode", 
                "messageDelivery.transport", "messageDelivery.httpIdleTimeoutMs", 
                "messageDelivery.websocketConnectTimeoutMs"
            ],
            "Terminal & Images": [
                "terminal.showImages", "terminal.imageWidthCells", "terminal.clearOnShrink", 
                "images.autoResize", "images.blockImages"
            ],
            "Shell": [
                "shell.shellPath", "shell.shellCommandPrefix", "shell.npmCommand"
            ],
            "Sessions": [
                "sessions.sessionDir"
            ],
            "Markdown": [
                "markdown.codeBlockIndent"
            ],
            "Resources": [
                "resources.packages", "resources.extensions", "resources.skills", 
                "resources.prompts", "resources.themes", "resources.enableSkillCommands"
            ],
            "Bedrock": [
                "bedrock.defaultTier"
            ]
        }
        
        default_settings = self.get_default_settings()
        
        for category, keys in categories.items():
            print(f"{category}:")
            for key in keys:
                # Handle nested keys
                parts = key.split(".")
                value = self.settings
                for part in parts:
                    value = value.get(part, "") if isinstance(value, dict) else ""
                
                # Get default value
                default_val = default_settings
                for part in parts:
                    default_val = default_val.get(part, "") if isinstance(default_val, dict) else ""
                
                # Format the value nicely
                if isinstance(value, str):
                    formatted_value = f"'{value}'"
                elif isinstance(value, bool):
                    formatted_value = str(value).lower()
                elif isinstance(value, list):
                    formatted_value = str(value) if value else "[]"
                elif value == "":
                    formatted_value = "''"
                else:
                    formatted_value = str(value)
                
                # Highlight if it differs from default
                if value == default_val:
                    status = "(default)"
                else:
                    status = "*(modified)*"
                    
                print(f"  {key:40} = {formatted_value:20} {status}")
            print()
    
    def list_available_models(self) -> None:
        """List available models for the current provider."""
        provider = self.settings.get("model", {}).get("defaultProvider", "anthropic")
        
        if provider == "anthropic":
            models = [
                "claude-3-5-sonnet-20240620",
                "claude-3-opus-20240229",
                "claude-3-haiku-20240307",
                "claude-2.1",
                "claude-2.0"
            ]
            print(f"Available models for {provider}:\n")
            for i, model in enumerate(models, 1):
                print(f"  {i}. {model}")
        
        elif provider == "openai":
            models = [
                "gpt-4-turbo",
                "gpt-4",
                "gpt-3.5-turbo",
                "gpt-4o"
            ]
            print(f"Available models for {provider}:\n")
            for i, model in enumerate(models, 1):
                print(f"  {i}. {model}")
        
        elif provider == "google":
            models = [
                "gemini-pro",
                "gemini-pro-vision",
                "chat-bison"
            ]
            print(f"Available models for {provider}:\n")
            for i, model in enumerate(models, 1):
                print(f"  {i}. {model}")
        
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
            print(f"Available models for {provider}:\n")
            for i, model in enumerate(models, 1):
                print(f"  {i}. {model}")
        
        else:
            print(f"No model listing available for provider: {provider}")
    
    def set_bedrock_tier(self, tier: str) -> None:
        """Set the Bedrock pricing tier.
        
        Args:
            tier: One of 'flex', 'standard', 'spot'
        """
        valid_tiers = ["flex", "standard", "spot"]
        if tier not in valid_tiers:
            print(f"Invalid tier: {tier}. Valid options: {', '.join(valid_tiers)}")
            return
        
        self.settings.setdefault('bedrock', {})['defaultTier'] = tier
        self.save_settings()
        print(f"Bedrock tier set to: {tier}")
        
        # Provide additional guidance
        if tier == "flex":
            print("Tip: 'flex' tier is pay-per-request and recommended for variable workloads")
        elif tier == "standard":
            print("Tip: 'standard' tier is pay-per-vCPU-second and recommended for consistent workloads")
        elif tier == "spot":
            print("Tip: 'spot' tier is cheapest but instances can be interrupted")
    
    def get_provider(self) -> str:
        """Get the current provider.
        
        Returns:
            The current default provider
        """
        return self.settings.get("model", {}).get("defaultProvider", "anthropic")
    
    def get_thinking_level(self) -> str:
        """Get the current thinking level.
        
        Returns:
            The current default thinking level
        """
        return self.settings.get("model", {}).get("defaultThinkingLevel", "medium")
    
    def get_theme(self) -> str:
        """Get the current theme.
        
        Returns:
            The current theme
        """
        return self.settings.get("ui", {}).get("theme", "dark")
    
    def get_bedrock_tier(self) -> str:
        """Get the current Bedrock tier.
        
        Returns:
            The current Bedrock tier
        """
        return self.settings.get("bedrock", {}).get("defaultTier", "flex")
    
    def set_value(self, key_path: str, value: Any) -> bool:
        """Set a value in the settings using dot notation.
        
        Args:
            key_path: Dot-separated path to the setting (e.g., "ui.theme")
            value: Value to set
            
        Returns:
            True if successful, False otherwise
        """
        try:
            parts = key_path.split(".")
            target = self.settings
            
            # Navigate to the parent of the target
            for part in parts[:-1]:
                if part not in target:
                    target[part] = {}
                target = target[part]
            
            # Set the value
            target[parts[-1]] = value
            self.save_settings()
            logger.info(f"Set {key_path} = {value}")
            return True
        except Exception as e:
            logger.error(f"Error setting {key_path}: {e}")
            return False
    
    def get_value(self, key_path: str, default: Any = None) -> Any:
        """Get a value from the settings using dot notation.
        
        Args:
            key_path: Dot-separated path to the setting (e.g., "ui.theme")
            default: Default value if key not found
            
        Returns:
            The value at the key path, or default if not found
        """
        try:
            parts = key_path.split(".")
            target = self.settings
            
            for part in parts:
                if isinstance(target, dict) and part in target:
                    target = target[part]
                else:
                    return default
            
            return target
        except Exception as e:
            logger.error(f"Error getting {key_path}: {e}")
            return default
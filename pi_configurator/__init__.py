"""
Pi-Ckl - Main Package

A robust, modular configuration tool for the Pi Coding Agent.
"""

__version__ = "1.0.0"
__author__ = "Pi-Ckl Team"
__license__ = "MIT"
__all__ = [
    'ConfigManager',
    'InteractiveHandler',
    'TUIHandler',
    'SimpleTUIHandler',
    'ProviderManager',
    'DependencyManager'
]

# Import core components
from .core.config_manager import ConfigManager
from .tui.interactive_handler import InteractiveHandler
from .tui.tui_handler import TUIHandler
from .tui.simple_tui_handler import SimpleTUIHandler
from .providers.provider_manager import ProviderManager
from .utils.dependencies import DependencyManager
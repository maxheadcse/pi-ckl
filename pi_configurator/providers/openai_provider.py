"""
OpenAI Provider Integration
"""

from typing import List, Dict, Any
from .base_provider import BaseProvider

class OpenAIProvider(BaseProvider):
    """OpenAI provider integration."""
    
    def __init__(self):
        super().__init__()
        self.name = "openai"
        self.display_name = "OpenAI"
        self.requires_api_key = True
        self.supports_real_time_listing = True
        self.models = [
            {
                'id': 'gpt-4-turbo',
                'name': 'GPT-4 Turbo',
                'max_tokens': 128000,
                'context_window': 128000,
                'pricing': {'input': 0.01, 'output': 0.03, 'unit': 'per 1K tokens'}
            },
            {
                'id': 'gpt-4',
                'name': 'GPT-4',
                'max_tokens': 8192,
                'context_window': 8192,
                'pricing': {'input': 0.03, 'output': 0.06, 'unit': 'per 1K tokens'}
            },
            {
                'id': 'gpt-3.5-turbo',
                'name': 'GPT-3.5 Turbo',
                'max_tokens': 16385,
                'context_window': 16385,
                'pricing': {'input': 0.001, 'output': 0.002, 'unit': 'per 1K tokens'}
            }
        ]
"""
Google Provider Integration
"""

from typing import List, Dict, Any
from .base_provider import BaseProvider

class GoogleProvider(BaseProvider):
    """Google provider integration."""
    
    def __init__(self):
        super().__init__()
        self.name = "google"
        self.display_name = "Google"
        self.requires_api_key = True
        self.supports_real_time_listing = True
        self.models = [
            {
                'id': 'gemini-pro',
                'name': 'Gemini Pro',
                'max_tokens': 32768,
                'context_window': 32768
            },
            {
                'id': 'gemini-pro-vision',
                'name': 'Gemini Pro Vision',
                'max_tokens': 12288,
                'context_window': 12288
            }
        ]
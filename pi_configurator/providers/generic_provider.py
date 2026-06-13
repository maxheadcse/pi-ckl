"""
Generic Provider
"""

from typing import List, Dict, Any
from .base_provider import BaseProvider

class GenericProvider(BaseProvider):
    """Generic provider for unknown providers."""
    
    def __init__(self):
        super().__init__()
        self.name = "generic"
        self.display_name = "Generic Provider"
        self.requires_api_key = False
        self.supports_real_time_listing = False
        self.models = []
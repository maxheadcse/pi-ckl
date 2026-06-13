"""
Base Provider Class
"""

from typing import List, Dict, Any

class BaseProvider:
    """Base class for all providers."""
    
    def __init__(self):
        self.name = "generic"
        self.display_name = "Generic Provider"
        self.models = []
        self.requires_api_key = False
        self.supports_real_time_listing = False
    
    def list_models(self, **kwargs) -> List[Dict[str, Any]]:
        """List available models."""
        return self.models
    
    def get_config(self) -> Dict[str, Any]:
        """Get provider-specific configuration."""
        return {
            'name': self.name,
            'display_name': self.display_name,
            'requires_api_key': self.requires_api_key,
            'supports_real_time_listing': self.supports_real_time_listing,
            'default_model': self.models[0]['id'] if self.models else None
        }
    
    def validate_credentials(self, **credentials) -> bool:
        """Validate credentials."""
        return True
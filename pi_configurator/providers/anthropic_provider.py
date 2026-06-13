"""
Anthropic Provider Integration
"""

import os
import requests
from typing import List, Dict, Any
from .base_provider import BaseProvider

class AnthropicProvider(BaseProvider):
    """Anthropic provider integration."""
    
    def __init__(self):
        super().__init__()
        self.name = "anthropic"
        self.display_name = "Anthropic"
        self.requires_api_key = True
        self.supports_real_time_listing = True
        self.models = [
            {
                'id': 'claude-3-5-sonnet-20240620',
                'name': 'Claude 3.5 Sonnet',
                'max_tokens': 200000,
                'context_window': 200000,
                'pricing': {'input': 0.003, 'output': 0.015, 'unit': 'per 1K tokens'}
            },
            {
                'id': 'claude-3-opus-20240229',
                'name': 'Claude 3 Opus',
                'max_tokens': 200000,
                'context_window': 200000,
                'pricing': {'input': 0.015, 'output': 0.075, 'unit': 'per 1K tokens'}
            },
            {
                'id': 'claude-3-haiku-20240307',
                'name': 'Claude 3 Haiku',
                'max_tokens': 200000,
                'context_window': 200000,
                'pricing': {'input': 0.00025, 'output': 0.00125, 'unit': 'per 1K tokens'}
            }
        ]
    
    def list_models(self, **kwargs) -> List[Dict[str, Any]]:
        """List available Anthropic models."""
        try:
            # Try to get real-time data from Anthropic API
            if self._can_use_anthropic_api():
                return self._list_models_from_api(**kwargs)
            else:
                return self.models
        except Exception as e:
            print(f"Error listing Anthropic models: {e}")
            return self.models
    
    def _can_use_anthropic_api(self) -> bool:
        """Check if Anthropic API is accessible."""
        api_key = os.environ.get('ANTHROPIC_API_KEY')
        return api_key is not None
    
    def _list_models_from_api(self, **kwargs) -> List[Dict[str, Any]]:
        """List models from Anthropic API."""
        api_key = os.environ.get('ANTHROPIC_API_KEY')
        url = "https://api.anthropic.com/v1/models"
        
        try:
            headers = {
                'Authorization': f'Bearer {api_key}',
                'Content-Type': 'application/json',
                'Anthropic-Version': '2023-06-01'
            }
            
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            
            api_models = response.json().get('data', [])
            return [
                {
                    'id': model['id'],
                    'name': model.get('name', model['id']),
                    'created': model.get('created'),
                    'owned_by': model.get('owned_by')
                }
                for model in api_models
            ]
            
        except Exception as e:
            print(f"Anthropic API error: {e}")
            return self.models
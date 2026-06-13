"""
Provider Integration Module
Handles real-time model listings and provider-specific configurations
"""

import os
import json
import requests
from typing import List, Dict, Any, Optional
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ProviderManager:
    """Manages provider integrations and model listings."""
    
    def __init__(self):
        """Initialize the provider manager."""
        from .anthropic_provider import AnthropicProvider
        from .openai_provider import OpenAIProvider
        from .google_provider import GoogleProvider
        from .aws_bedrock_provider import AWSBedrockProvider
        from .generic_provider import GenericProvider
        
        self.providers = {
            'anthropic': AnthropicProvider(),
            'openai': OpenAIProvider(),
            'google': GoogleProvider(),
            'aws-bedrock': AWSBedrockProvider()
        }
    
    def get_provider(self, provider_name: str) -> 'BaseProvider':
        """Get a provider instance."""
        return self.providers.get(provider_name.lower(), GenericProvider())
    
    def list_models(self, provider_name: str, **kwargs) -> List[Dict[str, Any]]:
        """List models for a specific provider."""
        provider = self.get_provider(provider_name)
        return provider.list_models(**kwargs)
    
    def get_provider_config(self, provider_name: str) -> Dict[str, Any]:
        """Get provider-specific configuration."""
        provider = self.get_provider(provider_name)
        return provider.get_config()
    
    def validate_credentials(self, provider_name: str, **credentials) -> bool:
        """Validate provider credentials."""
        provider = self.get_provider(provider_name)
        return provider.validate_credentials(**credentials)

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

class AWSBedrockProvider(BaseProvider):
    """AWS Bedrock provider integration."""
    
    def __init__(self):
        super().__init__()
        self.name = "aws-bedrock"
        self.display_name = "AWS Bedrock"
        self.requires_api_key = True  # AWS credentials
        self.supports_real_time_listing = True
        self.models = []
        self._load_static_models()
    
    def _load_static_models(self):
        """Load static model list as fallback."""
        self.models = [
            {
                'id': 'anthropic.claude-3-5-sonnet-20240620-v1:0',
                'name': 'Claude 3.5 Sonnet',
                'provider': 'anthropic',
                'max_tokens': 200000,
                'context_window': 200000,
                'pricing': {'input': 0.003, 'output': 0.015, 'unit': 'per 1K tokens'}
            },
            {
                'id': 'anthropic.claude-3-opus-20240229-v1:0',
                'name': 'Claude 3 Opus',
                'provider': 'anthropic',
                'max_tokens': 200000,
                'context_window': 200000,
                'pricing': {'input': 0.015, 'output': 0.075, 'unit': 'per 1K tokens'}
            },
            {
                'id': 'anthropic.claude-3-haiku-20240307-v1:0',
                'name': 'Claude 3 Haiku',
                'provider': 'anthropic',
                'max_tokens': 200000,
                'context_window': 200000,
                'pricing': {'input': 0.00025, 'output': 0.00125, 'unit': 'per 1K tokens'}
            },
            {
                'id': 'amazon.titan-text-express-v1',
                'name': 'Titan Text Express',
                'provider': 'amazon',
                'max_tokens': 8192,
                'context_window': 8192,
                'pricing': {'input': 0.002, 'output': 0.004, 'unit': 'per 1K tokens'}
            },
            {
                'id': 'meta.llama3-70b-instruct-v1:0',
                'name': 'Llama 3 70B Instruct',
                'provider': 'meta',
                'max_tokens': 8192,
                'context_window': 8192,
                'pricing': {'input': 0.00795, 'output': 0.01056, 'unit': 'per 1K tokens'}
            },
            {
                'id': 'meta.llama3-8b-instruct-v1:0',
                'name': 'Llama 3 8B Instruct',
                'provider': 'meta',
                'max_tokens': 8192,
                'context_window': 8192,
                'pricing': {'input': 0.00095, 'output': 0.00126, 'unit': 'per 1K tokens'}
            }
        ]
    
    def list_models(self, use_cache: bool = True, **kwargs) -> List[Dict[str, Any]]:
        """List available Bedrock models."""
        try:
            # Try to use boto3 for real-time listing
            if self._can_use_boto3():
                return self._list_models_with_boto3()
            else:
                logger.info("boto3 not available or not configured, using static model list")
                return self.models
        except Exception as e:
            logger.error(f"Error listing Bedrock models: {e}")
            return self.models
    
    def _can_use_boto3(self) -> bool:
        """Check if boto3 is available and configured."""
        try:
            import boto3
            # Check if AWS credentials are available
            session = boto3.Session()
            credentials = session.get_credentials()
            return credentials is not None
        except ImportError:
            return False
        except Exception:
            return False
    
    def _list_models_with_boto3(self) -> List[Dict[str, Any]]:
        """List models using boto3."""
        import boto3
        
        try:
            # Initialize Bedrock client
            bedrock = boto3.client('bedrock')
            
            # List foundation models
            response = bedrock.list_foundation_models()
            
            models = []
            for model in response.get('modelSummaries', []):
                models.append({
                    'id': model['modelId'],
                    'name': model.get('modelName', model['modelId']),
                    'provider': model.get('providerName', 'unknown'),
                    'input_modality': model.get('inputModality', []),
                    'output_modality': model.get('outputModality', []),
                    'model_arn': model.get('modelArn'),
                    'creation_time': model.get('creationTime'),
                    'customizations': model.get('customizationsSupported', [])
                })
            
            return models
            
        except Exception as e:
            logger.error(f"boto3 error: {e}")
            return self.models
    
    def get_config(self) -> Dict[str, Any]:
        """Get Bedrock-specific configuration."""
        config = super().get_config()
        config.update({
            'pricing_tiers': ['flex', 'standard', 'spot'],
            'default_tier': 'flex',
            'regions': ['us-east-1', 'us-west-2', 'eu-west-1', 'ap-southeast-1'],
            'recommended_tier': 'flex'
        })
        return config
    
    def validate_credentials(self, **credentials) -> bool:
        """Validate AWS credentials."""
        try:
            import boto3
            # Try to create a client with provided credentials
            session = boto3.Session(
                aws_access_key_id=credentials.get('aws_access_key_id'),
                aws_secret_access_key=credentials.get('aws_secret_access_key'),
                region_name=credentials.get('region_name', 'us-east-1')
            )
            
            # Test with a simple call
            sts = session.client('sts')
            sts.get_caller_identity()
            return True
            
        except ImportError:
            return False
        except Exception as e:
            logger.error(f"AWS credential validation failed: {e}")
            return False

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
            logger.error(f"Error listing Anthropic models: {e}")
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
            logger.error(f"Anthropic API error: {e}")
            return self.models

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

class GenericProvider(BaseProvider):
    """Generic provider for unknown providers."""
    
    def __init__(self):
        super().__init__()
        self.name = "generic"
        self.display_name = "Generic Provider"
        self.requires_api_key = False
        self.supports_real_time_listing = False
        self.models = []

# Global provider manager instance
provider_manager = ProviderManager()

if __name__ == "__main__":
    # Test the provider manager
    pm = ProviderManager()
    
    print("Testing Provider Manager:")
    print("=" * 50)
    
    for provider_name in ['anthropic', 'openai', 'google', 'aws-bedrock']:
        provider = pm.get_provider(provider_name)
        models = provider.list_models()
        print(f"\n{provider.display_name}:")
        print(f"  Models: {len(models)}")
        print(f"  Requires API Key: {provider.requires_api_key}")
        print(f"  Supports Real-time: {provider.supports_real_time_listing}")
        if models:
            print(f"  Example: {models[0]['name']}")
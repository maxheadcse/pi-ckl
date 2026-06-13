"""
AWS Bedrock Provider Integration
"""

import os
import logging
from typing import List, Dict, Any
from .base_provider import BaseProvider

logger = logging.getLogger(__name__)

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
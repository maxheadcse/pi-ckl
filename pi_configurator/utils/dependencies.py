"""
Dependency Management Utilities

Handles checking and managing optional dependencies.
"""

import importlib
import sys
import subprocess
from typing import List, Dict, Tuple

class DependencyManager:
    """Manages optional dependencies and provides fallback functionality."""
    
    # Define required and optional dependencies
    REQUIRED_DEPENDENCIES = [
        ('rich', 'Rich console formatting'),
    ]
    
    OPTIONAL_DEPENDENCIES = {
        'providers': [
            ('boto3', 'AWS Bedrock integration'),
            ('requests', 'HTTP requests for provider APIs'),
        ],
        'tui': [
            ('textual', 'Advanced TUI features'),
        ],
        'serialization': [
            ('pyyaml', 'YAML configuration support'),
        ]
    }
    
    @classmethod
    def check_dependency(cls, module_name: str) -> bool:
        """Check if a dependency is available."""
        try:
            importlib.import_module(module_name)
            return True
        except ImportError:
            return False
    
    @classmethod
    def check_all_dependencies(cls) -> Dict[str, bool]:
        """Check all dependencies and return availability status."""
        result = {}
        
        # Check required dependencies
        for module, description in cls.REQUIRED_DEPENDENCIES:
            result[module] = cls.check_dependency(module)
        
        # Check optional dependencies
        for category, deps in cls.OPTIONAL_DEPENDENCIES.items():
            for module, description in deps:
                result[f"{category}.{module}"] = cls.check_dependency(module)
        
        return result
    
    @classmethod
    def get_missing_dependencies(cls) -> List[Tuple[str, str]]:
        """Get list of missing required dependencies."""
        missing = []
        for module, description in cls.REQUIRED_DEPENDENCIES:
            if not cls.check_dependency(module):
                missing.append((module, description))
        return missing
    
    @classmethod
    def get_optional_dependencies_status(cls) -> Dict[str, Dict[str, bool]]:
        """Get status of optional dependencies."""
        status = {}
        for category, deps in cls.OPTIONAL_DEPENDENCIES.items():
            status[category] = {}
            for module, description in deps:
                status[category][module] = cls.check_dependency(module)
        return status
    
    @classmethod
    def install_dependency(cls, module_name: str) -> bool:
        """Attempt to install a missing dependency."""
        try:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', module_name])
            return True
        except subprocess.CalledProcessError:
            return False
        except Exception:
            return False
    
    @classmethod
    def install_missing_required(cls) -> bool:
        """Install all missing required dependencies."""
        missing = cls.get_missing_dependencies()
        if not missing:
            return True
        
        print(f"Installing {len(missing)} missing required dependencies...")
        success = True
        for module, description in missing:
            print(f"  Installing {module} ({description})...")
            if cls.install_dependency(module):
                print(f"  ✅ Successfully installed {module}")
            else:
                print(f"  ❌ Failed to install {module}")
                success = False
        
        return success
    
    @classmethod
    def check_and_warn(cls) -> None:
        """Check dependencies and warn about missing ones."""
        missing_required = cls.get_missing_dependencies()
        optional_status = cls.get_optional_dependencies_status()
        
        if missing_required:
            print("⚠️  Missing required dependencies:")
            for module, description in missing_required:
                print(f"  • {module}: {description}")
            print("\nSome features may not work properly.")
            print("Run 'pip install " + " ".join([m[0] for m in missing_required]) + "' to install them.")
        
        # Check for optional dependencies that could enhance functionality
        print("\n💡 Optional dependencies for enhanced functionality:")
        for category, deps in optional_status.items():
            print(f"  {category}:")
            for module, available in deps.items():
                status = "✅" if available else "🔄"
                print(f"    {status} {module}")

# Global dependency manager instance
dep_manager = DependencyManager()

if __name__ == "__main__":
    # Test dependency checking
    print("Dependency Status:")
    print("=" * 50)
    
    dep_manager.check_and_warn()
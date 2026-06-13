# Changelog

All notable changes to the Pi Coding Agent Configuration Tool will be documented in this file.

## [1.0.0] - 2026-06-13

### Added
- Initial release of the Pi Coding Agent Configuration Tool
- Complete CLI interface with all major configuration options
- Interactive menu-driven configuration system with 14 menu options
- Configuration management with JSON storage
- Support for multiple AI providers (Anthropic, OpenAI, Google, AWS Bedrock)
- Model listing functionality for each provider
- AWS Bedrock pricing tier configuration (flex, standard, spot)
- Comprehensive settings management for all Pi Coding Agent features

### Features
- **CLI Mode**: Full command-line interface for all configuration options
- **Interactive Mode**: Menu-driven configuration with easy navigation
- **Configuration Management**: JSON-based settings storage with validation
- **Multi-Provider Support**: Configure different AI providers and models
- **Bedrock Support**: AWS Bedrock pricing tier configuration
- **Error Handling**: Robust error handling and user feedback
- **Input Validation**: Comprehensive input validation for all settings

### Fixed
- Fixed broken Python files (core.py, interactive.py)
- Fixed argument parsing conflicts in main.py
- Fixed incomplete method implementations
- Fixed code structure and organization issues

### Changed
- Rewrote interactive.py with proper structure and complete functionality
- Enhanced core.py with proper error handling and validation
- Improved main.py with better argument parsing and error handling
- Added version information and proper module documentation

### Technical Improvements
- Added proper exception handling throughout the codebase
- Implemented input validation for all user inputs
- Added comprehensive logging for debugging and monitoring
- Improved code organization and modularity
- Added proper type hints and docstrings
- Enhanced error messages and user feedback

## [Unreleased]

### Planned Features
- Additional CLI arguments for all settings
- Configuration profiles and presets
- Import/export configuration functionality
- Configuration validation and linting
- Interactive configuration wizard
- Configuration diff and merge tools
- Configuration backup and restore functionality
- Configuration versioning and migration

### Known Issues
- Some Makefile targets reference CLI arguments not yet implemented in main.py
- Interactive mode could benefit from more user-friendly navigation
- Additional input validation could be added for edge cases

## Contributing

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct and the process for submitting pull requests.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact

For questions, issues, or contributions, please visit the [GitHub repository](https://github.com/maxheadcse/pi-configurator).
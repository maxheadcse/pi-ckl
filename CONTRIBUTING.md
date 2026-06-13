# Contributing to Pi Coding Agent Configuration Tool

Thank you for your interest in contributing to the Pi Coding Agent Configuration Tool! We welcome contributions from the community.

## Code of Conduct

By participating in this project, you agree to abide by our [Code of Conduct](CODE_OF_CONDUCT.md).

## How Can I Contribute?

### Reporting Bugs

- **Search existing issues** before creating a new one
- **Use a clear and descriptive title** for the issue
- **Provide detailed steps to reproduce** the issue
- **Include relevant information** such as:
  - Operating system and version
  - Python version
  - Exact error messages
  - Screenshots if applicable

### Suggesting Enhancements

- **Search existing issues** before suggesting a new feature
- **Use a clear and descriptive title** for the feature request
- **Provide a detailed description** of the proposed feature
- **Explain why this feature would be useful**
- **Include examples or mockups** if applicable

### Pull Requests

1. **Fork the repository** and create your branch from `master`
2. **Follow the coding standards** described below
3. **Write comprehensive tests** for new features
4. **Update documentation** as needed
5. **Submit a pull request** with a clear description of changes

## Development Setup

### Prerequisites

- Python 3.8+
- pip (Python package manager)
- git

### Installation

```bash
# Clone the repository
git clone https://github.com/maxheadcse/pi-configurator.git
cd pi-configurator

# Install dependencies
pip install -r requirements.txt

# Install development dependencies
pip install -r requirements-dev.txt
```

### Running Tests

```bash
# Run all tests
python -m pytest

# Run tests with coverage
python -m pytest --cov=config

# Run specific test
python -m pytest tests/test_core.py
```

## Coding Standards

### Python Code

- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) style guide
- Use type hints for function signatures
- Write comprehensive docstrings
- Keep functions focused and single-purpose
- Use meaningful variable and function names

### Documentation

- Update README.md for new features
- Add examples for new functionality
- Keep CHANGELOG.md up to date
- Write clear, concise commit messages

### Commit Messages

- Use present tense ("Add feature" not "Added feature")
- Limit first line to 72 characters
- Reference issues when applicable (e.g., "Fixes #123")
- Use bullet points for multiple changes

## Project Structure

```
pi-configurator/
├── config/                  # Core configuration modules
│   ├── core.py             # Configuration management
│   ├── cli.py              # CLI handling
│   └── interactive.py      # Interactive menu system
├── main.py                 # Main entry point
├── configurator.sh         # Shell script wrapper
├── setup.py                # Package installation
├── requirements.txt        # Production dependencies
├── requirements-dev.txt    # Development dependencies
├── README.md               # Project documentation
├── CHANGELOG.md            # Change history
├── CONTRIBUTING.md         # Contribution guidelines
├── LICENSE                 # License information
└── Makefile                # Convenience targets
```

## Versioning

We use [Semantic Versioning](https://semver.org/) for this project:

- **MAJOR** version when you make incompatible API changes
- **MINOR** version when you add functionality in a backwards-compatible manner
- **PATCH** version when you make backwards-compatible bug fixes

## Release Process

1. Update CHANGELOG.md with release notes
2. Update version in setup.py
3. Create a new Git tag: `git tag v1.0.0`
4. Push the tag: `git push origin v1.0.0`
5. Create a GitHub release with release notes

## Community

- **GitHub Issues**: For bug reports and feature requests
- **GitHub Discussions**: For general questions and discussions
- **Pull Requests**: For code contributions

## License

By contributing to this project, you agree that your contributions will be licensed under the [MIT License](LICENSE).

## Questions?

If you have any questions about contributing, please open an issue or contact the maintainers.

Thank you for contributing to the Pi Coding Agent Configuration Tool! 🚀
#!/usr/bin/env bash

# Pi-Ckl - Configuration Tool for Pi Coding Agent
# A robust, menu-driven and CLI-capable configuration tool

# Set strict mode
set -euo pipefail

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

# Check if Python 3 is available
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is required but not found."
    echo "Please install Python 3 and try again."
    exit 1
fi

# Check and install required packages
check_packages() {
    local missing_packages=0
    
    # Check for required packages (non-aggressive check)
    for package in rich; do  # Only rich is truly required
        if ! python3 -c "import $package" &> /dev/null; then
            echo "Warning: Required package '$package' not found."
            echo "For full functionality, please install it with:"
            echo "  pip install $package"
            echo ""
            missing_packages=1
        fi
    done
    
    # Check for optional packages (informational only)
    for package in pyyaml; do
        if ! python3 -c "import $package" &> /dev/null; then
            echo "Info: Optional package '$package' not found."
            echo "Some features may be enhanced with: pip install $package"
            echo ""
        fi
    done
}

# Parse command line arguments
INTERACTIVE_MODE=false
CONFIG_DIR=""
SETTINGS_FILE=""
SHOW_HELP=false

while [[ $# -gt 0 ]]; do
    case "$1" in
        -i|--interactive)
            INTERACTIVE_MODE=true
            shift
            ;;
        -c|--config-dir)
            CONFIG_DIR="$2"
            shift 2
            ;;
        -s|--settings)
            SETTINGS_FILE="$2"
            shift 2
            ;;
        -h|--help)
            SHOW_HELP=true
            shift
            ;;
        --*)
            # Pass through other arguments to Python script
            PYTHON_ARGS+=("$1")
            shift
            ;;
        *)
            echo "Unknown option: $1"
            SHOW_HELP=true
            break
            ;;
    esac
done

# Show help if requested
if [[ "$SHOW_HELP" == true ]]; then
    echo "Pi-Ckl - Configuration Tool for Pi Coding Agent"
    echo ""
    echo "Usage: $0 [OPTIONS]"
    echo ""
    echo "Options:"
    echo "  -i, --interactive      Run interactive menu-driven configuration"
    echo "  -c, --config-dir DIR   Override config directory (default: ~/.pi/agent)"
    echo "  -s, --settings FILE    Use specific settings file path"
    echo "  --list                 List all available settings and their values"
    echo "  --list-models          List available models for current provider"
    echo "  --default-bedrock-tier TIER"
    echo "                         AWS Bedrock pricing tier: flex, standard, spot"
    echo "  -h, --help            Show this help message and exit"
    echo ""
    echo "Examples:"
    echo "  $0 --interactive           # Start interactive configuration"
    echo "  $0 --list                  # List all settings"
    echo "  $0 --default-bedrock-tier flex"
    echo "                         # Set Bedrock tier to flex"
    exit 0
fi

# Check for required packages
check_packages

# Build Python arguments
PYTHON_ARGS=()
if [[ "$INTERACTIVE_MODE" == true ]]; then
    PYTHON_ARGS+=("--interactive")
fi

if [[ -n "$CONFIG_DIR" ]]; then
    PYTHON_ARGS+=("--config-dir" "$CONFIG_DIR")
fi

if [[ -n "$SETTINGS_FILE" ]]; then
    PYTHON_ARGS+=("--settings" "$SETTINGS_FILE")
fi

# Run the Python script
python3 "$SCRIPT_DIR/main.py" "${PYTHON_ARGS[@]}" "$@"

# Exit with the same status as the Python script
exit $?
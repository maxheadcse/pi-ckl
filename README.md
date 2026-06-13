# Pi-Ckl - Configuration Tool for Pi Coding Agent

A robust, modular, and secure configuration tool for the Pi Coding Agent with menu-driven interface and CLI capabilities.

![Pi Coding Agent Configuration Tool](https://via.placeholder.com/600x400?text=Pi+Coding+Agent+Configuration+Tool)

## Overview

This is a complete redesign of the Pi Coding Agent Configuration Tool with a modern Python-based architecture. It provides both a menu-driven interactive interface and comprehensive command-line capabilities for configuring the Pi Coding Agent.

## Features

- ✅ **Menu-driven configuration interface** - Interactive text-based menu for easy configuration
- ✅ **CLI capabilities** - All configuration options available via command-line
- ✅ **Model listing** - List available AI models from various providers
- ✅ **AWS Bedrock support** - Configure pricing tiers (flex, standard, spot)
- ✅ **JSON configuration storage** - Persistent, schema-validated configuration
- ✅ **Modular architecture** - Clean separation of concerns with dedicated components
- ✅ **Security-focused** - No hardcoded secrets, configuration stored securely
- ✅ **Easy to use** - Intuitive interface for both beginners and advanced users

## Installation

```bash
cd /path/to/pi-configurator
pip install -r requirements.txt
```

Or add to your PATH:

```bash
chmod +x configurator.sh
cp configurator.sh /usr/local/bin/pi-config
```

## Usage

### Interactive Mode (Default)

Simply run the script without arguments to enter interactive mode:

```bash
# Full interactive configuration
./configurator.sh

# Or use the Python directly
python3 main.py --interactive

# Use a specific config directory
./configurator.sh --config-dir /custom/path

# Use a specific settings file
./configurator.sh --settings /path/to/settings.json
```

### CLI Mode

```bash
# Set multiple defaults
python3 main.py \
  --default-theme light \
  --default-thinking-level high \
  --no-hide-thinking-block \
  --default-project-trust always

# Save to a custom location
python3 main.py --default-theme dark -s /custom/settings.json
```

### Help and Options

```bash
# Show help
python3 main.py --help

# List all available settings
python3 main.py --list

# List available models for current provider
python3 main.py --list-models

# Set Bedrock tier to flex
python3 main.py --default-bedrock-tier flex
```

## Command Line Options

| Option | Short | Description |
|--------|-------|-------------|
| `--interactive` | `-i` | Run in interactive mode with prompts |
| `--config-dir` | `-c` | Override config directory (default: `~/.pi/agent`) |
| `--settings` | `-s` | Use specific settings file path |
| `--default-<key>` | - | Set a default value for a setting |
| `--no-<key>` | - | Set a setting to false |
| `--list` | - | List all available settings |
| `--list-models` | - | List available models for current provider |
| `--default-bedrock-tier` | - | Set AWS Bedrock pricing tier (flex, standard, spot) |
| `--help` | `-h` | Show help message |
| `--help` | `-h` | Show help message |

## Available Settings

### Model & Thinking

| Setting | Type | Default | Description |
|---------|------|---------|-------------|
| `defaultProvider` | string | - | Default provider (anthropic, openai, google, etc.) |
| `defaultModel` | string | - | Default model ID |
| `defaultThinkingLevel` | string | `medium` | Thinking level: off, minimal, low, medium, high, xhigh |
| `hideThinkingBlock` | boolean | `false` | Hide thinking blocks in output |

### UI & Display

| Setting | Type | Default | Description |
|---------|------|---------|-------------|
| `theme` | string | `dark` | Theme name (dark, light, or custom) |
| `quietStartup` | boolean | `false` | Hide startup header |
| `defaultProjectTrust` | string | `ask` | Trust behavior: ask, always, never |
| `collapseChangelog` | boolean | `false` | Show condensed changelog after updates |
| `enableInstallTelemetry` | boolean | `true` | Send anonymous install/update ping |
| `doubleEscapeAction` | string | `tree` | Action for double-escape: tree, fork, none |
| `treeFilterMode` | string | `default` | Default filter for /tree |
| `editorPaddingX` | number | `0` | Horizontal padding for input editor |
| `autocompleteMaxVisible` | number | `5` | Max visible items in autocomplete |
| `showHardwareCursor` | boolean | `false` | Show terminal cursor while TUI positions |

### Compaction

| Setting | Type | Default | Description |
|---------|------|---------|-------------|
| `compaction.enabled` | boolean | `true` | Enable auto-compaction |
| `compaction.reserveTokens` | number | `16384` | Tokens reserved for LLM response |
| `compaction.keepRecentTokens` | number | `20000` | Recent tokens to keep |

### Retry

| Setting | Type | Default | Description |
|---------|------|---------|-------------|
| `retry.enabled` | boolean | `true` | Enable automatic retry on transient errors |
| `retry.maxRetries` | number | `3` | Maximum retry attempts |
| `retry.baseDelayMs` | number | `2000` | Base delay for exponential backoff |

### Message Delivery

| Setting | Type | Default | Description |
|---------|------|---------|-------------|
| `steeringMode` | string | `one-at-a-time` | How steering messages are sent |
| `followUpMode` | string | `one-at-a-time` | How follow-up messages are sent |
| `transport` | string | `auto` | Preferred transport: auto, sse, websocket, websocket-cached |
| `httpIdleTimeoutMs` | number | `300000` | HTTP idle timeout in milliseconds |
| `websocketConnectTimeoutMs` | number | `15000` | WebSocket connect timeout |

### Terminal & Images

| Setting | Type | Default | Description |
|---------|------|---------|-------------|
| `terminal.showImages` | boolean | `true` | Show images in terminal |
| `terminal.imageWidthCells` | number | `60` | Preferred inline image width |
| `terminal.clearOnShrink` | boolean | `false` | Clear empty rows when content shrinks |
| `images.autoResize` | boolean | `true` | Resize images to max 2000x2000 |
| `images.blockImages` | boolean | `false` | Block all images from being sent to LLM |

### Shell

| Setting | Type | Default | Description |
|---------|------|---------|-------------|
| `shell.shellPath` | string | - | Custom shell path |
| `shell.shellCommandPrefix` | string | - | Prefix for every bash command |
| `shell.npmCommand` | array | - | npm command argv |

### Sessions

| Setting | Type | Default | Description |
|---------|------|---------|-------------|
| `sessions.sessionDir` | string | - | Directory where session files are stored |

### Markdown

| Setting | Type | Default | Description |
|---------|------|---------|-------------|
| `markdown.codeBlockIndent` | string | `  ` | Indentation for code blocks |

### Resources

| Setting | Type | Default | Description |
|---------|------|---------|-------------|
| `resources.packages` | array | `[]` | npm/git packages to load resources from |
| `resources.extensions` | array | `[]` | Local extension file paths or directories |
| `resources.skills` | array | `[]` | Local skill file paths or directories |
| `resources.prompts` | array | `[]` | Local prompt template paths or directories |
| `resources.themes` | array | `[]` | Local theme file paths or directories |
| `resources.enableSkillCommands` | boolean | `true` | Register skills as /skill:name commands |

### Model Cycling

| Setting | Type | Default | Description |
|---------|------|---------|-------------|
| `enabledModels` | array | `[]` | Model patterns for Ctrl+P cycling |

## Examples

### Set a Light Theme with High Thinking

```bash
python main.py --default-theme light --default-thinking-level high
```

### Disable Telemetry and Hide Thinking Blocks

```bash
python main.py --no-enable-install-telemetry --no-hide-thinking-block
```

### Configure Project Trust

```bash
python main.py --default-project-trust always
```

### Full Configuration with Custom Settings File

```bash
python main.py --settings /custom/settings.json \
  --default-theme dark \
  --default-thinking-level medium \
  --default-project-trust ask
```

### Interactive Configuration

```bash
python main.py --interactive

# Or with a specific config directory
python main.py --config-dir /custom/path --interactive
```

### Configure Bedrock Pricing Tier

```bash
# Set flex tier (pay per request, recommended)
python main.py --default-bedrock-tier flex

# Set standard tier (pay per vCPU-second)
python main.py --default-bedrock-tier standard

# Set spot tier (cheapest, but can be interrupted)
python main.py --default-bedrock-tier spot
```

### List Available Models

```bash
python main.py --list-models
```

## Notes

- Settings are saved to `~/.pi/agent/settings.json` by default
- CLI defaults override existing settings
- Both dash notation (`--default-project-trust`) and camelCase (`--defaultProjectTrust`) are supported
- Boolean flags use `--no-<setting>` to set to `false`
- Array settings (packages, extensions, etc.) can be set as comma-separated values

## Bedrock Support

Configure AWS Bedrock pricing tier:

| Tier | Description | Recommendation |
|------|-------------|----------------|
| flex | Pay per request | Recommended for variable workloads |
| standard | Pay per vCPU-second | Recommended for consistent workloads |
| spot | Cheapest, but can be interrupted | For cost-sensitive workloads |

Use `--default-bedrock-tier flex` to set the recommended tier.

```bash
# Set to flex (recommended)
python main.py --default-bedrock-tier flex

# Set to standard
python main.py --default-bedrock-tier standard

# Set to spot (cheapest)
python main.py --default-bedrock-tier spot
```

## License

MIT License

© 2026 Pi-Ckl Team

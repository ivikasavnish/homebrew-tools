# Homebrew Tools Tap

Custom Homebrew formulas for developer productivity and safety.

```bash
brew tap ivikasavnish/tools
```

---

## safe-rm

A safe `rm` wrapper that prevents accidental file deletions by AI agents and humans.

### Features

- **3-Step Confirmation**: Type full path → Solve math puzzle (7-digit) → Type DELETE
- **Trash System**: Moves to `~/.safe-rm-trash` instead of deleting (kept 7 days)
- **Path Restrictions**: Only `~/`, `~/Documents`, `~/Downloads` allowed
- **System Protection**: Blocks `/`, `/usr`, `/bin`, `/etc`, and other system directories
- **MCP Server**: Model Context Protocol server for AI agent integration
- **Auto-Inject**: One-command injection into Claude Desktop, VS Code, Cursor, Windsurf, Zed

---

## Quick Start

### Install

```bash
# Via Homebrew
brew install ivikasavnish/tools/safe-rm
safe-rm install
source ~/.zshrc

# Via curl (one-liner)
curl -fsSL https://gist.githubusercontent.com/ivikasavnish/6336e16d11659980e70bd0403131bb54/raw/safe-rm | bash -s install
```

### Inject MCP into AI Editors

```bash
safe-rm --inject       # Interactive menu
safe-rm --inject-all   # Auto-inject all detected editors
```

### Uninstall

```bash
safe-rm --uninstall    # Restore default rm
brew uninstall safe-rm # Remove formula
brew untap ivikasavnish/tools
```

---

## Commands Reference

### Deletion (Requires User Confirmation)

| Command | Description |
|---------|-------------|
| `rm -rf <path>` | Safe deletion with 3-step confirmation |
| `rm -r <path>` | Same as above for directories |
| `rm <file>` | Delete single file |

### Trash Management

| Command | Description |
|---------|-------------|
| `rm --list-trash` | View all items in trash |
| `rm --restore <id>` | Restore item to original location |
| `rm --destroy <id>` | Permanently delete from trash |
| `rm --empty-trash` | Permanently delete all trash |
| `rm --clean-old` | Remove items older than 7 days |

### Installation & Status

| Command | Description |
|---------|-------------|
| `safe-rm install` | Install and shadow `/bin/rm` |
| `rm --status` | Show installation status |
| `rm --uninstall` | Restore default rm behavior |

### AI/MCP Integration

| Command | Description |
|---------|-------------|
| `rm --inject` | Interactive menu to inject MCP |
| `rm --inject-all` | Auto-inject into all editors |
| `rm --mcp-server` | Run MCP server directly |

### Bypass (Use Real rm)

| Command | Description |
|---------|-------------|
| `real-rm <args>` | Alias to real rm |
| `/bin/rm <args>` | Direct path to system rm |

---

## MCP Server Integration

The MCP (Model Context Protocol) server allows AI agents to safely interact with the file system.

### Supported Editors

| Editor | Config Location |
|--------|-----------------|
| Claude Desktop | `~/Library/Application Support/Claude/claude_desktop_config.json` |
| VS Code | `~/.vscode/globalStorage/anthropic.claude-code/settings/mcp.json` |
| Cursor | `~/.cursor/mcp.json` |
| Windsurf | `~/.windsurf/mcp.json` |
| Zed | `~/.config/zed/mcp.json` |
| Global | `~/.mcp/config.json` |

### MCP Tools Available to AI Agents

| Tool | AI Can Execute | Description |
|------|----------------|-------------|
| `safe_rm_list_trash` | ✅ Yes | List deleted items |
| `safe_rm_restore` | ✅ Yes | Restore from trash |
| `safe_rm_status` | ✅ Yes | Check installation |
| `safe_rm_clean_old` | ✅ Yes | Clean old items |
| `safe_rm_trash_info` | ✅ Yes | Get item details |
| `safe_rm_request_delete` | ✅ Yes | Returns instructions for user |

### Manual MCP Configuration

If auto-inject doesn't work, add this to your editor's MCP config:

```json
{
  "mcpServers": {
    "safe-rm": {
      "command": "python3",
      "args": ["/Users/YOUR_USERNAME/bin/safe-rm-mcp-server.py"],
      "env": {
        "SAFE_RM_PATH": "/Users/YOUR_USERNAME/bin/safe-rm"
      }
    }
  }
}
```

---

## AI Agent Instructions

### Add to CLAUDE.md or System Prompt

```markdown
## File Deletion Policy (safe-rm)

This system uses safe-rm for file deletion safety.

### Safe Commands (AI can execute)
- `rm --list-trash` - View deleted items
- `rm --restore <id>` - Restore from trash
- `rm --status` - Check installation
- `rm --clean-old` - Clean old trash items

### User-Only Commands (require confirmation)
- `rm -rf <path>` - Requires: path + math + DELETE
- `rm --destroy <id>` - Requires: DESTROY
- `rm --empty-trash` - Requires: DESTROY ALL

### NEVER Use (blocked)
- `/bin/rm` - Bypasses safety
- `real-rm` - Bypasses safety
```

### Skills JSON

Fetch machine-readable skills definition:

```bash
curl -fsSL https://gist.githubusercontent.com/ivikasavnish/6336e16d11659980e70bd0403131bb54/raw/safe-rm-skills.json
```

---

## How It Works

### Deletion Flow

```
User runs: rm -rf ~/Downloads/temp
                    │
                    ▼
    ┌───────────────────────────────┐
    │  STEP 1: Type Full Path       │
    │  ~/Downloads/temp             │
    └───────────────────────────────┘
                    │
                    ▼
    ┌───────────────────────────────┐
    │  STEP 2: Solve Math Puzzle    │
    │  3847291 + 5192847 = ?        │
    └───────────────────────────────┘
                    │
                    ▼
    ┌───────────────────────────────┐
    │  STEP 3: Type "DELETE"        │
    └───────────────────────────────┘
                    │
                    ▼
    ┌───────────────────────────────┐
    │  Moved to Trash (7 days)      │
    │  ~/.safe-rm-trash/            │
    │  20240115_143022_temp         │
    └───────────────────────────────┘
```

### Path Restrictions

**Allowed:**
- `~/` (home directory contents, not home itself)
- `~/Documents/*`
- `~/Downloads/*`

**Blocked:**
- `/` (root)
- `/bin`, `/sbin`, `/usr`, `/etc`, `/var`, `/tmp`, `/opt`
- `/System`, `/Library`, `/Applications` (macOS)
- `/private`, `/cores`, `/dev`
- `$HOME` itself

---

## Files & Locations

| File | Location | Description |
|------|----------|-------------|
| safe-rm | `~/bin/safe-rm` | Main script |
| rm (shadow) | `~/bin/rm` | Symlink to safe-rm |
| MCP Server | `~/bin/safe-rm-mcp-server.py` | MCP protocol server |
| Trash | `~/.safe-rm-trash/` | Deleted items |
| Log | `~/.safe-rm-trash/.deletion-log` | Deletion history |

---

## Resources

| Resource | URL |
|----------|-----|
| **Gist** | https://gist.github.com/ivikasavnish/6336e16d11659980e70bd0403131bb54 |
| **Tap Repo** | https://github.com/ivikasavnish/homebrew-tools |
| **Skills JSON** | [safe-rm-skills.json](safe-rm-skills.json) |
| **Agent Guide** | [safe-rm-agent-skills.md](safe-rm-agent-skills.md) |

---

## License

MIT

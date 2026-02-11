# Homebrew Tools Tap

Custom Homebrew formulas.

## Installation

```bash
brew tap ivikasavnish/tools
```

## Available Formulas

### safe-rm

A safe `rm` wrapper that prevents accidental deletions by AI agents and humans.

**Features:**
- Requires typing full path to confirm
- Requires solving math puzzle (7-digit addition)
- Moves to trash instead of deleting (kept 7 days)
- Only allows deletion under `~/`, `~/Documents`, `~/Downloads`
- Blocks root and system directories
- Provides restore and permanent delete options
- **AI Agent Skills**: Agents can list/restore trash but cannot delete

**Install:**
```bash
brew install ivikasavnish/tools/safe-rm
safe-rm install
source ~/.zshrc
```

**Uninstall:**
```bash
safe-rm --uninstall
brew uninstall safe-rm
```

## AI Agent Integration

### Commands Safe for AI Agents

| Command | Description |
|---------|-------------|
| `rm --list-trash` | View trash contents |
| `rm --restore <id>` | Restore from trash |
| `rm --status` | Check installation |
| `rm --help` | Show help |
| `rm --clean-old` | Clean items >7 days |

### Commands Requiring User Interaction

| Command | Why |
|---------|-----|
| `rm -rf <path>` | Requires path + math + DELETE |
| `rm --destroy <id>` | Requires DESTROY |
| `rm --empty-trash` | Requires DESTROY ALL |

### Add to Your AI Agent Config

**CLAUDE.md / System Prompt:**
```markdown
## File Deletion Policy
This system uses safe-rm for file deletion safety.
- Safe to run: rm --list-trash, rm --restore <id>, rm --status
- User must run: rm -rf <path> (requires interactive confirmation)
- NEVER use /bin/rm or bypass methods
```

**Skills JSON:**
```bash
curl -fsSL https://gist.githubusercontent.com/ivikasavnish/6336e16d11659980e70bd0403131bb54/raw/safe-rm-skills.json
```

## Resources

- **Gist**: https://gist.github.com/ivikasavnish/6336e16d11659980e70bd0403131bb54
- **Skills Guide**: [safe-rm-agent-skills.md](safe-rm-agent-skills.md)
- **Skills JSON**: [safe-rm-skills.json](safe-rm-skills.json)

## Install Methods

| Method | Command |
|--------|---------|
| **Homebrew** | `brew install ivikasavnish/tools/safe-rm && safe-rm install` |
| **curl** | `curl -fsSL https://gist.githubusercontent.com/ivikasavnish/6336e16d11659980e70bd0403131bb54/raw/safe-rm \| bash -s install` |

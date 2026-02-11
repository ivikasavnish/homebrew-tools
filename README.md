# Homebrew Tools Tap

Custom Homebrew formulas.

## Installation

```bash
brew tap ivikasavnish/tools
```

## Available Formulas

### safe-rm

A safe `rm` wrapper that prevents accidental deletions.

**Features:**
- Requires typing full path to confirm
- Requires solving math puzzle (7-digit addition)
- Moves to trash instead of deleting (kept 7 days)
- Only allows deletion under `~/`, `~/Documents`, `~/Downloads`
- Blocks root and system directories
- Provides restore and permanent delete options

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

**Usage:**
```bash
rm -rf ~/Downloads/folder   # Safe deletion with prompts
rm --list-trash             # View trash
rm --restore <id>           # Restore from trash
rm --destroy <id>           # Permanently delete from trash
rm --status                 # Check installation status
rm --uninstall              # Restore default rm
real-rm <args>              # Bypass (use real rm)
```

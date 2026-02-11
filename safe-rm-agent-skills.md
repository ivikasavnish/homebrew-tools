# safe-rm AI Agent Skills

Instructions for AI agents (Claude, GPT, Copilot, etc.) to safely interact with the file deletion system.

## CRITICAL RULES

1. **NEVER** use `/bin/rm`, `real-rm`, or any bypass method
2. **NEVER** attempt to automate the confirmation steps (path typing, math puzzle)
3. **NEVER** pipe input to rm commands
4. **ALWAYS** inform the user when deletion is needed and let them handle it manually

## Available Commands (Safe for AI Agents)

### View Trash Contents
```bash
rm --list-trash
```
Use this to see what items are in the trash, their original paths, and trash IDs.

### Restore from Trash
```bash
rm --restore <TRASH_ID>
```
Restore a previously deleted item. Get the TRASH_ID from `--list-trash`.

### Check Installation Status
```bash
rm --status
```
Verify safe-rm is properly installed and active.

### Clean Old Trash Items
```bash
rm --clean-old
```
Remove items older than 7 days from trash (runs automatically but can be triggered manually).

### View Help
```bash
rm --help
```
Show all available options.

## Commands Requiring User Interaction

These commands **CANNOT** be automated by AI agents:

| Command | Why |
|---------|-----|
| `rm -rf <path>` | Requires interactive confirmation (path + math + DELETE) |
| `rm --destroy <id>` | Requires typing "DESTROY" |
| `rm --empty-trash` | Requires typing "DESTROY ALL" |

## Recommended AI Agent Behavior

### When User Asks to Delete Files

```
User: "Delete the temp folder"

CORRECT Response:
"To delete ~/Downloads/temp, please run:
  rm -rf ~/Downloads/temp

You'll need to:
1. Type the full path to confirm
2. Solve a math problem
3. Type 'DELETE'

The folder will be moved to trash for 7 days."

INCORRECT Response:
[Attempting to run rm -rf directly or bypassing safety]
```

### When User Asks to Recover Files

```
User: "I accidentally deleted my project folder"

CORRECT Response:
"Let me check the trash for your folder."
[Run: rm --list-trash]
"Found it! To restore, run:
  rm --restore 20240115_143022_project

Or I can restore it for you - this command is safe for me to run."
[Run: rm --restore 20240115_143022_project]
```

### When User Asks to Permanently Delete from Trash

```
User: "Permanently delete item X from trash"

CORRECT Response:
"To permanently delete, please run:
  rm --destroy 20240115_143022_item

You'll need to type 'DESTROY' to confirm.
This action cannot be undone."

INCORRECT Response:
[Attempting to run --destroy directly]
```

## Path Restrictions

AI agents should be aware these paths are protected:

**Allowed (under user home only):**
- `~/` (home directory contents)
- `~/Documents/*`
- `~/Downloads/*`

**Blocked:**
- `/` (root)
- `/bin`, `/sbin`, `/usr`, `/etc`, `/var`, `/tmp`, `/opt`
- `/System`, `/Library`, `/Applications` (macOS)
- `/private`, `/cores`, `/dev`
- `$HOME` itself (cannot delete home directory)

## Integration Examples

### For Claude Code / Anthropic Agents

Add to CLAUDE.md or system prompt:
```markdown
## File Deletion Policy

This system uses safe-rm. When deleting files:
1. Use `rm --list-trash` to view deleted items (safe to run)
2. Use `rm --restore <id>` to recover files (safe to run)
3. For actual deletion, inform user to run `rm -rf <path>` manually
4. NEVER use /bin/rm or bypass methods
```

### For GitHub Copilot / VS Code Agents

```json
{
  "safe-rm.rules": {
    "allowedCommands": ["rm --list-trash", "rm --restore", "rm --status", "rm --help", "rm --clean-old"],
    "blockedCommands": ["rm -rf", "rm --destroy", "rm --empty-trash", "/bin/rm", "real-rm"],
    "requireUserConfirmation": ["rm -rf", "rm --destroy", "rm --empty-trash"]
  }
}
```

### For Custom AI Agents

```python
SAFE_RM_SKILLS = {
    "safe_commands": [
        "rm --list-trash",
        "rm --restore {trash_id}",
        "rm --status",
        "rm --help",
        "rm --clean-old"
    ],
    "user_only_commands": [
        "rm -rf {path}",
        "rm --destroy {trash_id}",
        "rm --empty-trash"
    ],
    "blocked_commands": [
        "/bin/rm",
        "real-rm",
        "command rm",
        "\\rm"
    ]
}
```

## Skill Summary

| Skill | AI Can Execute | Notes |
|-------|----------------|-------|
| List trash | Yes | `rm --list-trash` |
| Restore item | Yes | `rm --restore <id>` |
| Check status | Yes | `rm --status` |
| Show help | Yes | `rm --help` |
| Clean old items | Yes | `rm --clean-old` |
| Delete files | No | User must confirm interactively |
| Destroy from trash | No | User must type DESTROY |
| Empty trash | No | User must type DESTROY ALL |
| Bypass safe-rm | **NEVER** | Blocked for safety |

# safe-rm AI Agent Skills

Complete guide for AI agents (Claude, GPT, Copilot, Gemini, etc.) to safely interact with the file deletion system.

---

## Quick Reference

| Action | Command | AI Can Execute |
|--------|---------|----------------|
| List trash | `rm --list-trash` | ✅ Yes |
| Restore file | `rm --restore <id>` | ✅ Yes |
| Check status | `rm --status` | ✅ Yes |
| Clean old items | `rm --clean-old` | ✅ Yes |
| Delete file | `rm -rf <path>` | ❌ No (user only) |
| Destroy from trash | `rm --destroy <id>` | ❌ No (user only) |
| Empty trash | `rm --empty-trash` | ❌ No (user only) |
| Bypass safe-rm | `/bin/rm` | 🚫 NEVER |

---

## Critical Rules for AI Agents

### MUST DO
1. Use `rm --list-trash` to view deleted items
2. Use `rm --restore <id>` to recover files
3. Inform users to run deletion commands manually
4. Explain the 3-step confirmation process

### MUST NOT
1. ❌ Use `/bin/rm`, `real-rm`, or any bypass method
2. ❌ Attempt to automate confirmation steps
3. ❌ Pipe input to rm commands
4. ❌ Use `echo` or `expect` to simulate user input
5. ❌ Execute `rm -rf` directly

---

## MCP Server Tools

When connected via MCP, these tools are available:

### safe_rm_list_trash
```json
{
  "name": "safe_rm_list_trash",
  "description": "List all items in trash with IDs and original paths",
  "inputSchema": { "type": "object", "properties": {}, "required": [] }
}
```

### safe_rm_restore
```json
{
  "name": "safe_rm_restore",
  "description": "Restore deleted item from trash",
  "inputSchema": {
    "type": "object",
    "properties": {
      "trash_id": { "type": "string", "description": "Trash ID from list_trash" }
    },
    "required": ["trash_id"]
  }
}
```

### safe_rm_status
```json
{
  "name": "safe_rm_status",
  "description": "Check safe-rm installation status",
  "inputSchema": { "type": "object", "properties": {}, "required": [] }
}
```

### safe_rm_clean_old
```json
{
  "name": "safe_rm_clean_old",
  "description": "Remove items older than 7 days from trash",
  "inputSchema": { "type": "object", "properties": {}, "required": [] }
}
```

### safe_rm_trash_info
```json
{
  "name": "safe_rm_trash_info",
  "description": "Get detailed info about a trash item",
  "inputSchema": {
    "type": "object",
    "properties": {
      "trash_id": { "type": "string", "description": "Trash ID" }
    },
    "required": ["trash_id"]
  }
}
```

### safe_rm_request_delete
```json
{
  "name": "safe_rm_request_delete",
  "description": "Request deletion - returns instructions for user",
  "inputSchema": {
    "type": "object",
    "properties": {
      "path": { "type": "string", "description": "Path to delete" }
    },
    "required": ["path"]
  }
}
```

---

## Example Interactions

### User Asks to Delete Files

**User:** "Delete the temp folder in Downloads"

**Correct AI Response:**
```
To delete ~/Downloads/temp, please run:

    rm -rf ~/Downloads/temp

You'll need to complete these steps:
1. Type the full path: /Users/you/Downloads/temp
2. Solve a math problem (e.g., 3847291 + 5192847 = ?)
3. Type 'DELETE'

The folder will be moved to trash for 7 days and can be restored if needed.
```

**Incorrect AI Response:**
```
❌ Running rm -rf ~/Downloads/temp...
```

---

### User Asks to Recover Files

**User:** "I accidentally deleted my project folder"

**Correct AI Response:**
```
Let me check the trash for your folder.

[Executes: rm --list-trash]

Found these items:
- 2024-01-15 14:30  ~/Documents/project  20240115_143022_project

To restore it, I'll run:

[Executes: rm --restore 20240115_143022_project]

Your project has been restored to ~/Documents/project
```

---

### User Asks to Permanently Delete

**User:** "Permanently delete item X from trash"

**Correct AI Response:**
```
To permanently delete from trash, please run:

    rm --destroy 20240115_143022_item

You'll need to type 'DESTROY' to confirm.

⚠️ This action cannot be undone.
```

---

## Path Restrictions

AI agents should validate paths before suggesting deletion:

### Allowed Paths
```
~/anything           ✅ (except ~/ itself)
~/Documents/...      ✅
~/Downloads/...      ✅
```

### Blocked Paths
```
/                    ❌ Root directory
/bin                 ❌ System binaries
/sbin                ❌ System binaries
/usr                 ❌ Unix system resources
/etc                 ❌ Configuration files
/var                 ❌ Variable data
/tmp                 ❌ Temporary files
/opt                 ❌ Optional packages
/System              ❌ macOS system
/Library             ❌ macOS library
/Applications        ❌ macOS applications
/private             ❌ macOS private
/cores               ❌ Core dumps
/dev                 ❌ Device files
~/                   ❌ Home directory itself
```

---

## Integration Configurations

### Claude Code (CLAUDE.md)

Add to your project's CLAUDE.md:

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

---

### VS Code / Cursor Settings

Add to `.vscode/settings.json` or workspace settings:

```json
{
  "claude.fileOperations": {
    "deleteCommand": "safe-rm",
    "requireConfirmation": true,
    "blockedCommands": ["/bin/rm", "real-rm"]
  }
}
```

---

### GitHub Copilot Instructions

Add to `.github/copilot-instructions.md`:

```markdown
## File Deletion

This repository uses safe-rm. When suggesting file deletions:
1. Never use /bin/rm or bypass commands
2. Suggest `rm -rf <path>` and explain the confirmation steps
3. Use `rm --list-trash` and `rm --restore` for recovery
```

---

### Custom AI Agent Integration

```python
SAFE_RM_CONFIG = {
    "safe_commands": [
        "rm --list-trash",
        "rm --restore {trash_id}",
        "rm --status",
        "rm --help",
        "rm --clean-old"
    ],
    "user_only_commands": [
        "rm -rf {path}",
        "rm -r {path}",
        "rm --destroy {trash_id}",
        "rm --empty-trash"
    ],
    "blocked_commands": [
        "/bin/rm",
        "/usr/bin/rm",
        "real-rm",
        "command rm",
        "\\rm",
        "env rm"
    ],
    "allowed_paths": [
        "$HOME/*",
        "$HOME/Documents/*",
        "$HOME/Downloads/*"
    ]
}
```

---

### OpenAI Function Calling

```json
{
  "functions": [
    {
      "name": "list_deleted_files",
      "description": "List files in safe-rm trash",
      "parameters": { "type": "object", "properties": {} }
    },
    {
      "name": "restore_file",
      "description": "Restore file from trash",
      "parameters": {
        "type": "object",
        "properties": {
          "trash_id": { "type": "string" }
        },
        "required": ["trash_id"]
      }
    },
    {
      "name": "request_file_deletion",
      "description": "Generate deletion instructions for user",
      "parameters": {
        "type": "object",
        "properties": {
          "path": { "type": "string" }
        },
        "required": ["path"]
      }
    }
  ]
}
```

---

## Troubleshooting

### "Command not found: rm"
The safe-rm alias may not be loaded. Run:
```bash
source ~/.zshrc  # or ~/.bashrc
```

### "Path not allowed"
The path is outside allowed directories. Only `~/`, `~/Documents/`, `~/Downloads/` are permitted.

### "MCP server not connecting"
1. Check if MCP server exists: `ls ~/bin/safe-rm-mcp-server.py`
2. Re-inject: `safe-rm --inject`
3. Restart your editor

### AI agent bypassing safe-rm
Report this as a safety issue. The agent should never use `/bin/rm` or `real-rm`.

---

## Resources

| Resource | URL |
|----------|-----|
| Main Script | `~/bin/safe-rm` |
| MCP Server | `~/bin/safe-rm-mcp-server.py` |
| Skills JSON | https://gist.githubusercontent.com/ivikasavnish/6336e16d11659980e70bd0403131bb54/raw/safe-rm-skills.json |
| GitHub Tap | https://github.com/ivikasavnish/homebrew-tools |

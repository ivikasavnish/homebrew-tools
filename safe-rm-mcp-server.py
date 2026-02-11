#!/usr/bin/env python3
"""
safe-rm MCP Server
Model Context Protocol server for safe file deletion operations

Run: python3 safe-rm-mcp-server.py
"""

import asyncio
import json
import os
import subprocess
import sys
from pathlib import Path
from datetime import datetime

# MCP Protocol Implementation (stdio-based)
SAFE_RM_PATH = os.environ.get('SAFE_RM_PATH', os.path.expanduser('~/bin/safe-rm'))
TRASH_DIR = Path.home() / '.safe-rm-trash'


def send_response(response: dict):
    """Send JSON-RPC response to stdout"""
    msg = json.dumps(response)
    sys.stdout.write(f"Content-Length: {len(msg)}\r\n\r\n{msg}")
    sys.stdout.flush()


def read_message():
    """Read JSON-RPC message from stdin"""
    headers = {}
    while True:
        line = sys.stdin.readline()
        if line == '\r\n' or line == '\n':
            break
        if ':' in line:
            key, value = line.split(':', 1)
            headers[key.strip()] = value.strip()

    content_length = int(headers.get('Content-Length', 0))
    if content_length > 0:
        content = sys.stdin.read(content_length)
        return json.loads(content)
    return None


def exec_safe_rm(args: str) -> str:
    """Execute safe-rm command and return output"""
    try:
        result = subprocess.run(
            f'"{SAFE_RM_PATH}" {args}',
            shell=True,
            capture_output=True,
            text=True,
            timeout=30
        )
        return result.stdout or result.stderr
    except subprocess.TimeoutExpired:
        return "Error: Command timed out"
    except Exception as e:
        return f"Error: {str(e)}"


def list_trash() -> dict:
    """List all items in trash"""
    output = exec_safe_rm('--list-trash')
    return {"content": [{"type": "text", "text": output}]}


def restore_from_trash(trash_id: str) -> dict:
    """Restore item from trash"""
    import re
    if not re.match(r'^[0-9]{8}_[0-9]{6}_[\w\-\.]+$', trash_id):
        return {"content": [{"type": "text", "text": "Error: Invalid trash_id format"}], "isError": True}

    output = exec_safe_rm(f'--restore "{trash_id}"')
    return {"content": [{"type": "text", "text": output or f"Restored: {trash_id}"}]}


def check_status() -> dict:
    """Check safe-rm status"""
    output = exec_safe_rm('--status')
    return {"content": [{"type": "text", "text": output}]}


def clean_old_trash() -> dict:
    """Clean old items from trash"""
    output = exec_safe_rm('--clean-old')
    return {"content": [{"type": "text", "text": output}]}


def get_trash_info(trash_id: str) -> dict:
    """Get info about specific trash item"""
    trash_path = TRASH_DIR / trash_id
    log_file = TRASH_DIR / '.deletion-log'

    if not trash_path.exists():
        return {"content": [{"type": "text", "text": f"Error: Item not found: {trash_id}"}], "isError": True}

    stats = trash_path.stat()
    original_path = "Unknown"

    if log_file.exists():
        for line in log_file.read_text().splitlines():
            if line.endswith(f"|{trash_id}"):
                original_path = line.split('|')[1]
                break

    info = {
        "trash_id": trash_id,
        "original_path": original_path,
        "type": "directory" if trash_path.is_dir() else "file",
        "deleted_date": datetime.fromtimestamp(stats.st_mtime).isoformat(),
        "size_bytes": stats.st_size
    }
    return {"content": [{"type": "text", "text": json.dumps(info, indent=2)}]}


def request_deletion(path: str) -> dict:
    """Request deletion - returns instructions for user"""
    abs_path = os.path.abspath(os.path.expanduser(path))
    msg = f"""⚠️ DELETION REQUEST

To delete: {abs_path}

I cannot delete files directly. Please run:

```bash
rm -rf "{abs_path}"
```

You will need to:
1. Type the full path to confirm
2. Solve a math problem (e.g., 3847291 + 5192847 = ?)
3. Type 'DELETE'

Item moves to trash for 7 days. Restore with:
```bash
rm --list-trash
rm --restore <trash_id>
```"""
    return {"content": [{"type": "text", "text": msg}]}


TOOLS = [
    {
        "name": "safe_rm_list_trash",
        "description": "List all items in the safe-rm trash with their IDs and original paths",
        "inputSchema": {"type": "object", "properties": {}, "required": []}
    },
    {
        "name": "safe_rm_restore",
        "description": "Restore a deleted item from trash to its original location",
        "inputSchema": {
            "type": "object",
            "properties": {"trash_id": {"type": "string", "description": "Trash ID from list_trash"}},
            "required": ["trash_id"]
        }
    },
    {
        "name": "safe_rm_status",
        "description": "Check safe-rm installation status",
        "inputSchema": {"type": "object", "properties": {}, "required": []}
    },
    {
        "name": "safe_rm_clean_old",
        "description": "Remove items older than 7 days from trash",
        "inputSchema": {"type": "object", "properties": {}, "required": []}
    },
    {
        "name": "safe_rm_trash_info",
        "description": "Get detailed info about a trash item",
        "inputSchema": {
            "type": "object",
            "properties": {"trash_id": {"type": "string", "description": "Trash ID"}},
            "required": ["trash_id"]
        }
    },
    {
        "name": "safe_rm_request_delete",
        "description": "Request file deletion - returns instructions for user to delete manually",
        "inputSchema": {
            "type": "object",
            "properties": {"path": {"type": "string", "description": "Path to delete"}},
            "required": ["path"]
        }
    }
]


def handle_request(request: dict) -> dict:
    """Handle incoming JSON-RPC request"""
    method = request.get('method', '')
    req_id = request.get('id')
    params = request.get('params', {})

    if method == 'initialize':
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "protocolVersion": "2024-11-05",
                "capabilities": {"tools": {}},
                "serverInfo": {"name": "safe-rm", "version": "1.0.0"}
            }
        }

    elif method == 'tools/list':
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {"tools": TOOLS}
        }

    elif method == 'tools/call':
        tool_name = params.get('name', '')
        args = params.get('arguments', {})

        handlers = {
            'safe_rm_list_trash': lambda: list_trash(),
            'safe_rm_restore': lambda: restore_from_trash(args.get('trash_id', '')),
            'safe_rm_status': lambda: check_status(),
            'safe_rm_clean_old': lambda: clean_old_trash(),
            'safe_rm_trash_info': lambda: get_trash_info(args.get('trash_id', '')),
            'safe_rm_request_delete': lambda: request_deletion(args.get('path', ''))
        }

        handler = handlers.get(tool_name)
        if handler:
            result = handler()
            return {"jsonrpc": "2.0", "id": req_id, "result": result}
        else:
            return {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32601, "message": f"Unknown tool: {tool_name}"}}

    elif method == 'notifications/initialized':
        return None  # No response for notifications

    return {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32601, "message": f"Unknown method: {method}"}}


def main():
    """Main MCP server loop"""
    sys.stderr.write("safe-rm MCP server starting...\n")
    sys.stderr.flush()

    while True:
        try:
            request = read_message()
            if request is None:
                continue

            response = handle_request(request)
            if response:
                send_response(response)

        except EOFError:
            break
        except Exception as e:
            sys.stderr.write(f"Error: {e}\n")
            sys.stderr.flush()


if __name__ == '__main__':
    main()

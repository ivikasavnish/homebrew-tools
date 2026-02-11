#!/usr/bin/env node
/**
 * safe-rm MCP Server
 * Model Context Protocol server for safe file deletion operations
 *
 * Install: npm install -g @anthropic/sdk
 * Run: node safe-rm-mcp-server.js
 */

const { Server } = require('@modelcontextprotocol/sdk/server/index.js');
const { StdioServerTransport } = require('@modelcontextprotocol/sdk/server/stdio.js');
const { execSync, exec } = require('child_process');
const path = require('path');
const fs = require('fs');

const SAFE_RM_PATH = process.env.SAFE_RM_PATH || path.join(process.env.HOME, 'bin', 'safe-rm');
const TRASH_DIR = path.join(process.env.HOME, '.safe-rm-trash');

class SafeRmMcpServer {
  constructor() {
    this.server = new Server(
      {
        name: 'safe-rm',
        version: '1.0.0',
      },
      {
        capabilities: {
          tools: {},
        },
      }
    );

    this.setupToolHandlers();
  }

  setupToolHandlers() {
    this.server.setRequestHandler('tools/list', async () => {
      return {
        tools: [
          {
            name: 'list_trash',
            description: 'List all items in the safe-rm trash. Shows deleted files with their original paths and trash IDs for restoration.',
            inputSchema: {
              type: 'object',
              properties: {},
              required: [],
            },
          },
          {
            name: 'restore_from_trash',
            description: 'Restore a previously deleted item from trash to its original location.',
            inputSchema: {
              type: 'object',
              properties: {
                trash_id: {
                  type: 'string',
                  description: 'The trash ID of the item to restore (from list_trash output)',
                },
              },
              required: ['trash_id'],
            },
          },
          {
            name: 'check_status',
            description: 'Check the safe-rm installation status and configuration.',
            inputSchema: {
              type: 'object',
              properties: {},
              required: [],
            },
          },
          {
            name: 'clean_old_trash',
            description: 'Remove items older than 7 days from trash.',
            inputSchema: {
              type: 'object',
              properties: {},
              required: [],
            },
          },
          {
            name: 'get_trash_info',
            description: 'Get information about a specific item in trash.',
            inputSchema: {
              type: 'object',
              properties: {
                trash_id: {
                  type: 'string',
                  description: 'The trash ID to get info about',
                },
              },
              required: ['trash_id'],
            },
          },
          {
            name: 'request_deletion',
            description: 'Request deletion of a file/directory. This does NOT delete - it returns instructions for the user to perform the deletion manually with required confirmations.',
            inputSchema: {
              type: 'object',
              properties: {
                path: {
                  type: 'string',
                  description: 'The path to request deletion for',
                },
              },
              required: ['path'],
            },
          },
        ],
      };
    });

    this.server.setRequestHandler('tools/call', async (request) => {
      const { name, arguments: args } = request.params;

      try {
        switch (name) {
          case 'list_trash':
            return this.listTrash();
          case 'restore_from_trash':
            return this.restoreFromTrash(args.trash_id);
          case 'check_status':
            return this.checkStatus();
          case 'clean_old_trash':
            return this.cleanOldTrash();
          case 'get_trash_info':
            return this.getTrashInfo(args.trash_id);
          case 'request_deletion':
            return this.requestDeletion(args.path);
          default:
            throw new Error(`Unknown tool: ${name}`);
        }
      } catch (error) {
        return {
          content: [
            {
              type: 'text',
              text: `Error: ${error.message}`,
            },
          ],
          isError: true,
        };
      }
    });
  }

  execSafeRm(args) {
    try {
      const result = execSync(`"${SAFE_RM_PATH}" ${args}`, {
        encoding: 'utf-8',
        timeout: 30000,
      });
      return result;
    } catch (error) {
      throw new Error(error.stderr || error.message);
    }
  }

  listTrash() {
    const output = this.execSafeRm('--list-trash');
    return {
      content: [
        {
          type: 'text',
          text: output,
        },
      ],
    };
  }

  restoreFromTrash(trashId) {
    if (!trashId) {
      throw new Error('trash_id is required');
    }
    // Validate trash_id format to prevent injection
    if (!/^[0-9]{8}_[0-9]{6}_[\w\-\.]+$/.test(trashId)) {
      throw new Error('Invalid trash_id format');
    }
    const output = this.execSafeRm(`--restore "${trashId}"`);
    return {
      content: [
        {
          type: 'text',
          text: output || `Successfully restored: ${trashId}`,
        },
      ],
    };
  }

  checkStatus() {
    const output = this.execSafeRm('--status');
    return {
      content: [
        {
          type: 'text',
          text: output,
        },
      ],
    };
  }

  cleanOldTrash() {
    const output = this.execSafeRm('--clean-old');
    return {
      content: [
        {
          type: 'text',
          text: output,
        },
      ],
    };
  }

  getTrashInfo(trashId) {
    if (!trashId) {
      throw new Error('trash_id is required');
    }

    const trashPath = path.join(TRASH_DIR, trashId);
    const logFile = path.join(TRASH_DIR, '.deletion-log');

    if (!fs.existsSync(trashPath)) {
      throw new Error(`Item not found in trash: ${trashId}`);
    }

    const stats = fs.statSync(trashPath);
    let originalPath = 'Unknown';

    if (fs.existsSync(logFile)) {
      const log = fs.readFileSync(logFile, 'utf-8');
      const lines = log.split('\n');
      for (const line of lines) {
        if (line.endsWith(`|${trashId}`)) {
          originalPath = line.split('|')[1];
          break;
        }
      }
    }

    const info = {
      trash_id: trashId,
      original_path: originalPath,
      type: stats.isDirectory() ? 'directory' : 'file',
      deleted_date: stats.mtime.toISOString(),
      size_bytes: stats.size,
    };

    return {
      content: [
        {
          type: 'text',
          text: JSON.stringify(info, null, 2),
        },
      ],
    };
  }

  requestDeletion(targetPath) {
    if (!targetPath) {
      throw new Error('path is required');
    }

    const absPath = path.resolve(targetPath);

    return {
      content: [
        {
          type: 'text',
          text: `⚠️ DELETION REQUEST

To delete: ${absPath}

I cannot delete files directly. The user must run this command and complete the confirmation steps:

\`\`\`bash
rm -rf "${absPath}"
\`\`\`

The user will need to:
1. Type the full path to confirm
2. Solve a math problem (e.g., 3847291 + 5192847 = ?)
3. Type 'DELETE'

The item will be moved to trash for 7 days and can be restored with:
\`\`\`bash
rm --list-trash
rm --restore <trash_id>
\`\`\``,
        },
      ],
    };
  }

  async run() {
    const transport = new StdioServerTransport();
    await this.server.connect(transport);
    console.error('safe-rm MCP server running');
  }
}

const server = new SafeRmMcpServer();
server.run().catch(console.error);

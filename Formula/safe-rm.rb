class SafeRm < Formula
  desc "Safe rm wrapper with MCP server for AI agents - requires confirmation, math puzzle, uses trash"
  homepage "https://github.com/ivikasavnish/homebrew-tools"
  url "https://raw.githubusercontent.com/ivikasavnish/homebrew-tools/main/safe-rm"
  version "1.1.1"
  license "MIT"

  sha256 "f2695354766dbebfa82fb34c8c8390fe063bffb796198255c718022abc91c84a"

  depends_on "python@3"

  def install
    bin.install "safe-rm"

    # Install MCP server from repo
    mcp_server_url = "https://raw.githubusercontent.com/ivikasavnish/homebrew-tools/main/safe-rm-mcp-server.py"
    mcp_server_path = bin/"safe-rm-mcp-server.py"

    system "curl", "-fsSL", mcp_server_url, "-o", mcp_server_path
    chmod 0755, mcp_server_path

    # Install skills JSON
    skills_url = "https://raw.githubusercontent.com/ivikasavnish/homebrew-tools/main/safe-rm-skills.json"
    (share/"safe-rm").mkpath
    system "curl", "-fsSL", skills_url, "-o", share/"safe-rm/safe-rm-skills.json"
  end

  def caveats
    <<~EOS
      To activate safe-rm as your default rm:

        safe-rm install

      To inject MCP server into AI editors (Claude Desktop, VS Code, Cursor, etc.):

        safe-rm --inject      # Interactive menu
        safe-rm --inject-all  # Auto-inject all

      After installation:
        source ~/.zshrc   # or ~/.bashrc

      Commands:
        rm -rf <path>       Safe deletion with confirmations
        rm --list-trash     View trash
        rm --restore <id>   Restore from trash
        rm --inject         Inject MCP into editors
        rm --status         Check status
        rm --uninstall      Restore default rm

      MCP Server: #{bin}/safe-rm-mcp-server.py
      Skills JSON: #{share}/safe-rm/safe-rm-skills.json

      Bypass: real-rm or /bin/rm
    EOS
  end

  test do
    assert_match "safe rm wrapper", shell_output("#{bin}/safe-rm --help")
  end
end

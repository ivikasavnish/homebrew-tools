class SafeRm < Formula
  desc "Safe rm wrapper with MCP server for AI agents - requires confirmation, math puzzle, uses trash"
  homepage "https://gist.github.com/ivikasavnish/6336e16d11659980e70bd0403131bb54"
  url "https://gist.githubusercontent.com/ivikasavnish/6336e16d11659980e70bd0403131bb54/raw/safe-rm"
  version "1.1.0"
  sha256 "f2695354766dbebfa82fb34c8c8390fe063bffb796198255c718022abc91c84a"
  license "MIT"

  depends_on "python@3"

  resource "mcp_server" do
    url "https://gist.githubusercontent.com/ivikasavnish/6336e16d11659980e70bd0403131bb54/raw/safe-rm-mcp-server.py"
    sha256 :no_check  # Raw gist URLs don't have stable hashes
  end

  resource "agent_skills" do
    url "https://gist.githubusercontent.com/ivikasavnish/6336e16d11659980e70bd0403131bb54/raw/safe-rm-skills.json"
    sha256 :no_check
  end

  def install
    bin.install "safe-rm"

    resource("mcp_server").stage do
      bin.install "safe-rm-mcp-server.py"
    end

    resource("agent_skills").stage do
      (share/"safe-rm").install "safe-rm-skills.json"
    end
  end

  def post_install
    # Create symlink for MCP server
    ln_sf bin/"safe-rm-mcp-server.py", bin/"safe-rm-mcp"
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
    assert_predicate bin/"safe-rm-mcp-server.py", :exist?
  end
end

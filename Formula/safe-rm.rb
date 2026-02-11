class SafeRm < Formula
  desc "Safe rm wrapper: requires confirmation, math puzzle, moves to trash"
  homepage "https://gist.github.com/ivikasavnish/6336e16d11659980e70bd0403131bb54"
  url "https://gist.githubusercontent.com/ivikasavnish/6336e16d11659980e70bd0403131bb54/raw/safe-rm"
  version "1.0.0"
  sha256 "e5b61e14a036099c1e8a35340bf8cca8934a297a7492dd96469f3cd69a916025"
  license "MIT"

  def install
    bin.install "safe-rm"
  end

  def post_install
    # Create the shadow symlink in Homebrew's bin
    ln_sf bin/"safe-rm", bin/"safe-rm-wrapper"
  end

  def caveats
    <<~EOS
      To activate safe-rm as your default rm, run:

        safe-rm install

      This will:
        - Create ~/bin/rm symlink to shadow /bin/rm
        - Add aliases to your shell config
        - Set up trash directory

      After installation, run:
        source ~/.zshrc   # or ~/.bashrc

      Commands:
        rm -rf <path>       Safe deletion with confirmations
        rm --list-trash     View trash
        rm --restore <id>   Restore from trash
        rm --status         Check status
        rm --uninstall      Restore default rm

      Bypass: real-rm or /bin/rm
    EOS
  end

  test do
    assert_match "safe rm wrapper", shell_output("#{bin}/safe-rm --help")
  end
end

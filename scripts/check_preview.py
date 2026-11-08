"""Validate the inline JavaScript used by the static GitHub Pages preview."""
from __future__ import annotations

import shutil
import subprocess
import tempfile
from html.parser import HTMLParser
from pathlib import Path


class InlineScriptParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self._inside_script = False
        self._current: list[str] = []
        self.scripts: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag == "script":
            self._inside_script = True
            self._current = []

    def handle_data(self, data: str) -> None:
        if self._inside_script:
            self._current.append(data)

    def handle_endtag(self, tag: str) -> None:
        if tag == "script" and self._inside_script:
            self.scripts.append("".join(self._current))
            self._current = []
            self._inside_script = False


def main() -> None:
    node = shutil.which("node")
    if node is None:
        raise SystemExit("Node.js is required to validate index.html inline JavaScript.")

    preview = Path("index.html")
    if not preview.is_file():
        raise SystemExit("index.html is missing from the repository root.")

    parser = InlineScriptParser()
    parser.feed(preview.read_text(encoding="utf-8"))
    parser.close()

    if not parser.scripts or not any(script.strip() for script in parser.scripts):
        raise SystemExit("No inline JavaScript was found in index.html.")

    with tempfile.TemporaryDirectory() as directory:
        script_path = Path(directory) / "preview.js"
        script_path.write_text("\n".join(parser.scripts), encoding="utf-8")
        subprocess.run([node, "--check", str(script_path)], check=True)

    print(f"Validated {len(parser.scripts)} inline script block(s) in index.html.")


if __name__ == "__main__":
    main()

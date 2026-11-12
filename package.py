"""Package dist/version.dll into a zip laid out for the Everwind game folder.

Usage: python package.py 0.2.0-beta   ->  EverwindFXCore-0.2.0-beta.zip
"""
import re
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent
GAME_DIR = "skyverse/Binaries/Win64/"


def crlf(text: str) -> bytes:
    return text.replace("\r\n", "\n").replace("\n", "\r\n").encode("utf-8")


def main() -> None:
    if len(sys.argv) != 2:
        sys.exit("usage: python package.py <version>")
    version = sys.argv[1]

    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    readme = readme.split("## Building from source")[0]
    readme = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", readme)
    readme += "\nSource code: https://github.com/mcirish3/EverwindFXCore\n"

    out = ROOT / f"EverwindFXCore-{version}.zip"
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        z.write(ROOT / "dist" / "version.dll", GAME_DIR + "version.dll")
        z.writestr(GAME_DIR + "EverwindFXCore.ini",
                   crlf((ROOT / "config" / "EverwindFXCore.ini").read_text(encoding="utf-8")))
        z.writestr("EverwindFXCore-README.txt", crlf(readme))
        z.writestr("EverwindFXCore-LICENSE.txt", crlf((ROOT / "LICENSE").read_text(encoding="utf-8")))
    print(f"Packaged {out.name}")


if __name__ == "__main__":
    main()

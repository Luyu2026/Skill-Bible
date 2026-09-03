#!/usr/bin/env python3
"""Export a DOCX to PDF with Word when available, otherwise LibreOffice."""

import argparse
import json
import platform
import shutil
import subprocess
import sys
from pathlib import Path


MAC_WORD_APPS = [
    Path("/Applications/Microsoft Word.app"),
    Path.home() / "Applications/Microsoft Word.app",
]
def detect():
    system = platform.system()
    result = {
        "system": system,
        "microsoft_word": False,
        "libreoffice": bool(shutil.which("soffice")),
    }
    if system == "Darwin":
        result["microsoft_word"] = any(path.exists() for path in MAC_WORD_APPS)
    elif system == "Windows":
        # COM is checked lazily at export time to avoid launching Office during
        # a capability check.
        try:
            import winreg
            for key, name in ((r"Word.Application\\CLSID", "microsoft_word"),):
                try:
                    winreg.OpenKey(winreg.HKEY_CLASSES_ROOT, key)
                    result[name] = True
                except FileNotFoundError:
                    pass
        except ImportError:
            pass
    return result


def export_with_word_macos(source, output):
    script = '''
on run argv
    set sourceFile to POSIX file (item 1 of argv)
    set outputFile to POSIX file (item 2 of argv)
    tell application "Microsoft Word"
        activate
        set sourceDocument to open sourceFile
        save as sourceDocument file name outputFile file format format PDF
        close sourceDocument saving no
    end tell
end run
'''
    subprocess.run(["osascript", "-e", script, str(source), str(output)], check=True)


def export_with_com(source, output, application):
    import win32com.client

    office = win32com.client.DispatchEx(application)
    office.Visible = False
    document = None
    try:
        document = office.Documents.Open(str(source))
        # 17 is the standard Office fixed-format value for PDF.
        document.ExportAsFixedFormat(str(output), 17)
    finally:
        if document is not None:
            document.Close(False)
        office.Quit()


def export_with_libreoffice(source, output):
    soffice = shutil.which("soffice")
    if not soffice:
        raise RuntimeError("LibreOffice is not installed")
    output.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run([
        soffice, "--headless", "--convert-to", "pdf",
        "--outdir", str(output.parent), str(source),
    ], check=True)
    generated = output.parent / f"{source.stem}.pdf"
    if generated != output:
        generated.replace(output)


def export(source, output, backend):
    capabilities = detect()
    system = capabilities["system"]
    selected = backend
    if selected == "auto":
        if capabilities["microsoft_word"]:
            selected = "microsoft-word"
        else:
            selected = "libreoffice"

    output.parent.mkdir(parents=True, exist_ok=True)
    if selected == "microsoft-word":
        if not capabilities["microsoft_word"]:
            raise RuntimeError("Microsoft Word is not available on this computer")
        if system == "Darwin":
            export_with_word_macos(source, output)
        elif system == "Windows":
            export_with_com(source, output, "Word.Application")
        else:
            raise RuntimeError("Microsoft Word automation is supported on macOS and Windows only")
    elif selected == "libreoffice":
        export_with_libreoffice(source, output)
    else:
        raise ValueError(f"Unknown backend: {selected}")

    if not output.exists() or output.stat().st_size == 0:
        raise RuntimeError("PDF export did not produce a usable file")
    return selected


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--detect", action="store_true")
    parser.add_argument("--input", type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument(
        "--backend",
        choices=("auto", "microsoft-word", "libreoffice"),
        default="auto",
    )
    args = parser.parse_args()
    if args.detect:
        print(json.dumps(detect(), ensure_ascii=False))
        return
    if not args.input or not args.output:
        parser.error("--input and --output are required unless --detect is used")
    if args.input.suffix.lower() != ".docx":
        parser.error("--input must be a .docx file")
    try:
        selected = export(args.input, args.output, args.backend)
    except Exception as error:
        print(json.dumps({"ok": False, "error": str(error)}, ensure_ascii=False), file=sys.stderr)
        raise SystemExit(2)
    print(json.dumps({"ok": True, "backend": selected, "output": str(args.output)}, ensure_ascii=False))


if __name__ == "__main__":
    main()

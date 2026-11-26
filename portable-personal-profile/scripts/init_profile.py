#!/usr/bin/env python3
"""Create an empty portable profile without overwriting existing files."""
import argparse
import shutil
from pathlib import Path

def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('directory', type=Path, help='New profile directory chosen by the user')
    a = p.parse_args()
    try:
        if a.directory.exists() or a.directory.is_symlink():
            p.error('Destination exists; choose a new directory to preserve its contents.')
        a.directory.parent.mkdir(parents=True, exist_ok=True)
        shutil.copytree(Path(__file__).resolve().parents[1] / 'templates' / 'profile', a.directory)
    except OSError as e:
        p.error('Cannot create profile: ' + str(e))
    print('Created empty profile; register sources before adding records.')

if __name__ == '__main__':
    main()

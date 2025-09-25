#!/usr/bin/env python3
import re, pathlib, shutil

ROOT = pathlib.Path(__file__).parent
FILES = [
    ROOT/"index.html",
    ROOT/"style.css",
    ROOT/"script.js",
]

def backup(path: pathlib.Path):
    bak = path.with_suffix(path.suffix + '.bak')
    if not bak.exists():
        shutil.copy2(path, bak)

def strip_html(text: str) -> str:
    return re.sub(r'<!--.*?-->', '', text, flags=re.DOTALL)

def strip_css(text: str) -> str:
    text = re.sub(r'/\*.*?\*/', '', text, flags=re.DOTALL)
    return '\n'.join(l.rstrip() for l in text.splitlines() if l.strip())

def strip_js(text: str) -> str:
    # Remove /* */ first
    text = re.sub(r'/\*.*?\*/', '', text, flags=re.DOTALL)
    out_lines = []
    for line in text.splitlines():
        stripped = ''
        i = 0
        in_s = None
        while i < len(line):
            ch = line[i]
            if in_s:
                stripped += ch
                if ch == '\\' and i+1 < len(line):
                    stripped += line[i+1]; i += 2; continue
                if ch == in_s:
                    in_s = None
                i += 1
            else:
                if ch in ('"', "'", '`'):
                    in_s = ch
                    stripped += ch
                    i += 1
                elif ch == '/' and i+1 < len(line) and line[i+1] == '/':
                    break  # comment start
                else:
                    stripped += ch
                    i += 1
        if stripped.strip():
            out_lines.append(stripped.rstrip())
    return '\n'.join(out_lines)

def process(path: pathlib.Path):
    txt = path.read_text(encoding='utf-8')
    if path.name.endswith('.html'):
        cleaned = strip_html(txt)
    elif path.name.endswith('.css'):
        cleaned = strip_css(txt)
    elif path.name.endswith('.js'):
        cleaned = strip_js(txt)
    else:
        return
    path.write_text(cleaned + '\n', encoding='utf-8')

if __name__ == '__main__':
    for f in FILES:
        if f.exists():
            backup(f)
            process(f)
    print('Stripped comments from frontend files (backups .bak created).')

#!/usr/bin/env python3
import re, pathlib, json, sys, os
from html import escape

ROOT = pathlib.Path(__file__).parent
DIST = ROOT / 'dist'
DIST.mkdir(exist_ok=True)

html = (ROOT / 'index.html').read_text(encoding='utf-8')
css = (ROOT / 'style.css').read_text(encoding='utf-8')
js = (ROOT / 'script.js').read_text(encoding='utf-8')
questions = (ROOT / 'questions.json').read_text(encoding='utf-8')

# naive minifiers
css_min = re.sub(r'/\*.*?\*/', '', css, flags=re.DOTALL)
css_min = re.sub(r'\s+', ' ', css_min)
css_min = re.sub(r' ?([{};:,]) ?', r'\1', css_min)
css_min = css_min.strip()

js_min = re.sub(r'/\*.*?\*/', '', js, flags=re.DOTALL)
# remove // comments preserving URLs: simple approach line by line
_min_lines = []
for line in js_min.split('\n'):
    if '//' in line:
        q = ''
        out = ''
        i=0
        in_s=None
        while i < len(line):
            ch=line[i]
            if in_s:
                out+=ch
                if ch=='\\' and i+1<len(line):
                    out+=line[i+1]; i+=2; continue
                if ch==in_s:
                    in_s=None
                i+=1
            else:
                if ch in ('"',"'",'`'):
                    in_s=ch; out+=ch; i+=1
                elif ch=='/' and i+1<len(line) and line[i+1]=='/':
                    break
                else:
                    out+=ch; i+=1
        line=out
    if line.strip():
        _min_lines.append(line)
js_min='\n'.join(_min_lines)
# collapse whitespace
js_min = re.sub(r'\s+', ' ', js_min)
# keep line breaks maybe minimal
js_min = js_min.strip()

# Inline CSS & JS into HTML clone
# replace link rel stylesheet and script src with inline
html_min = html
html_min = re.sub(r'<link[^>]*href="style.css"[^>]*>', f'<style>{css_min}</style>', html_min)
html_min = re.sub(r'<script src="script.js"></script>', f'<script>{js_min}</script>', html_min)

# write outputs
(ROOT/ 'dist' / 'index.html').write_text(html_min, encoding='utf-8')
(ROOT/ 'dist' / 'questions.json').write_text(questions, encoding='utf-8')
(ROOT/ 'dist' / 'script.min.js').write_text(js_min, encoding='utf-8')
(ROOT/ 'dist' / 'style.min.css').write_text(css_min, encoding='utf-8')
print('Dist build created: dist/index.html, inline assets plus separate minified files.')

if '--sizes' in sys.argv:
    def sz(p):
        return os.path.getsize(p)
    files = ['index.html','style.css','script.js','dist/index.html','dist/style.min.css','dist/script.min.js']
    print('\nSize report (bytes):')
    for f in files:
        if os.path.exists(f):
            print(f'{f}: {sz(f)}')

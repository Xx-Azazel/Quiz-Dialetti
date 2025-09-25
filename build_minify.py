#!/usr/bin/env python3
import re, pathlib, json, sys, os, hashlib
from html import escape

ROOT = pathlib.Path(__file__).parent
DIST = ROOT / 'dist'
DIST.mkdir(exist_ok=True)

html = (ROOT / 'index.html').read_text(encoding='utf-8')
css = (ROOT / 'style.css').read_text(encoding='utf-8')
js = (ROOT / 'script.js').read_text(encoding='utf-8')
questions = (ROOT / 'questions.json').read_text(encoding='utf-8')

css_min = re.sub(r'/\*.*?\*/', '', css, flags=re.DOTALL)
css_min = re.sub(r'\s+', ' ', css_min)
css_min = re.sub(r' ?([{};:,]) ?', r'\1', css_min)
css_min = css_min.strip()

js_min = re.sub(r'/\*.*?\*/', '', js, flags=re.DOTALL)
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
js_min = re.sub(r'\s+', ' ', js_min)
js_min = js_min.strip()

def digest(content: bytes, length=10):
    return hashlib.sha256(content).hexdigest()[:length]

css_hash = digest(css_min.encode('utf-8'))
js_hash = digest(js_min.encode('utf-8'))
questions_hash = digest(questions.encode('utf-8'))

hashed_css_name = f'style.{css_hash}.min.css'
hashed_js_name = f'script.{js_hash}.min.js'

html_hashed = re.sub(r'<link[^>]*href="style.css"[^>]*>', f'<link rel="stylesheet" href="{hashed_css_name}">', html)
html_hashed = re.sub(r'<script src="script.js"></script>', f'<script src="{hashed_js_name}" defer></script>', html_hashed)

meta_tag = f'\n    <meta name="x-questions-sha" content="{questions_hash}">'
if '</head>' in html_hashed:
    html_hashed = html_hashed.replace('</head>', meta_tag + '\n</head>')

html_inline = re.sub(r'<link[^>]*href="style.css"[^>]*>', f'<style>{css_min}</style>', html)
html_inline = re.sub(r'<script src="script.js"></script>', f'<script>{js_min}</script>', html_inline)
if '</head>' in html_inline:
    html_inline = html_inline.replace('</head>', meta_tag + '\n</head>')

dist_index = (DIST / 'index.html')
dist_inline = (DIST / 'index.inline.html')
(DIST / hashed_css_name).write_text(css_min, encoding='utf-8')
(DIST / hashed_js_name).write_text(js_min, encoding='utf-8')
(DIST / 'questions.json').write_text(questions, encoding='utf-8')
dist_index.write_text(html_hashed, encoding='utf-8')
dist_inline.write_text(html_inline, encoding='utf-8')
print('Dist build created:')
print(' -', dist_index.name, '(hashed assets)')
print(' -', dist_inline.name, '(inline variant)')
print(' -', hashed_css_name, hashed_js_name)
print('Questions hash:', questions_hash)

if '--sizes' in sys.argv:
    def sz(p):
        return os.path.getsize(p)
    files = ['index.html','style.css','script.js'] + [f'dist/{x}' for x in [dist_index.name, dist_inline.name, hashed_css_name, hashed_js_name, 'questions.json']]
    print('\nSize report (bytes):')
    for f in files:
        if os.path.exists(f):
            print(f'{f}: {sz(f)}')

#!/usr/bin/env python3
"""Check static showcase closure and declared asset budgets, not rendered usability."""
import argparse
from html.parser import HTMLParser
import json
import re
from pathlib import Path
from urllib.parse import urlsplit, unquote

class References(HTMLParser):
    def __init__(self): super().__init__(); self.refs=[]; self.ids=set()
    def handle_starttag(self,tag,attrs):
        attrs=dict(attrs)
        if 'id' in attrs:self.ids.add(attrs['id'])
        for key in ('href','src','poster'):
            if attrs.get(key):self.refs.append(attrs[key])
        if tag == 'script': raise ValueError('This showcase requires no script')

def check(root):
    root=root.resolve(); problems=[];references=0
    for document in sorted(root.rglob('*')):
        if document.suffix not in ('.html','.md'):continue
        text=document.read_text()
        if document.suffix=='.html':
            parser=References();parser.feed(text);refs=parser.refs
        else:refs=re.findall(r'\]\(([^)]+)\)',text)
        for ref in refs:
            references+=1;parts=urlsplit(ref);label=str(document.relative_to(root))+': '+ref
            if parts.scheme:
                if parts.scheme!='https':problems.append('Unsupported external reference: '+label)
                continue
            if parts.path.startswith('/'):problems.append('Root-relative URL breaks project prefix: '+label);continue
            target=(document.parent/unquote(parts.path)).resolve() if parts.path else document
            if not target.is_relative_to(root) or not target.is_file():problems.append('Missing or escaping reference: '+label)
            if document.suffix=='.html' and not parts.path and parts.fragment not in parser.ids:problems.append('Missing anchor: '+label)
    limits={'media/demo.mp4':25*1024*1024,'media/poster.jpg':500*1024,'media/demo.en.vtt':100*1024,'media/transcript.md':100*1024}
    for rel,limit in limits.items():
        if not (root/rel).is_file() or (root/rel).stat().st_size>limit:problems.append('Missing or oversized media: '+rel)
    files=list(root.rglob('*'))
    if any(p.is_symlink() for p in files):problems.append('Symlink in staged site')
    total=sum(p.stat().st_size for p in files if p.is_file())
    if total>35*1024*1024:problems.append('Site exceeds 35 MiB')
    if problems:raise ValueError('; '.join(problems))
    return {'valid':True,'references':references,'bytes':total,'limits':'All staged HTML/Markdown local references and byte budgets only; rendering, captions and playback require separate observations.'}

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('root',type=Path)
    try:print(json.dumps(check(parser.parse_args().root),indent=2))
    except (ValueError,OSError) as error:parser.exit(1,str(error)+'\n')

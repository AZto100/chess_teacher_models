#!/usr/bin/env python3
"""Rebuild fixed-puzzle HTML metadata. No npm or API key is needed."""
import argparse, html, json, re
from pathlib import Path
from urllib.parse import urlparse
ROOT=Path(__file__).resolve().parents[1]
def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--site',default='https://azto100.github.io/chess_teacher_models/',help='HTTPS repository/site URL, including its subdirectory.')
    ap.add_argument('--handle',default='',help='Your real X handle, e.g. @YourHandle; omitted when not supplied.')
    a=ap.parse_args();base=a.site.rstrip('/')+'/'
    if urlparse(base).scheme!='https' or not urlparse(base).netloc:ap.error('--site must be an absolute HTTPS URL')
    if a.handle and not re.fullmatch(r'@?[A-Za-z0-9_]{1,15}',a.handle):ap.error('Invalid X handle')
    handle='@'+a.handle.lstrip('@') if a.handle else ''
    esc=lambda s:html.escape(str(s),quote=True)
    records=[]
    for n in range(1,7):records+=json.loads((ROOT/'puzzles'/f'mate-{n}.json').read_text(encoding='utf-8'))['puzzles']
    (ROOT/'x-posts').mkdir(exist_ok=True)
    def page(p,alias=False):
        id=p['id'];title=f'{"White" if p["attacker"]=="w" else "Black"} to move. Mate in {p["mate"]}!'
        player=base+'x-player.html?p='+id;image=base+'images/'+id+'.jpg';canonical=base+('x-share.html' if alias else 'x-posts/'+id+'.html')
        meta={'twitter:card':'player','twitter:title':title,'twitter:description':'Solve the position against Stockfish 19 Lite. No hints. Try again without resetting the timer.', 'twitter:image':image,'twitter:image:alt':title+' Chess puzzle starting position.','twitter:player':player,'twitter:player:width':'480','twitter:player:height':'480'}
        if handle:meta['twitter:site']=handle
        tags='\n'.join(f'<meta name="{esc(k)}" content="{esc(v)}">' for k,v in meta.items())
        rel='' if alias else '../'
        return f'''<!doctype html>
<html lang="en"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{esc(title)}</title>
{tags}
<meta property="og:type" content="website"><meta property="og:title" content="{esc(title)}"><meta property="og:description" content="A timed chess puzzle. Can you find the mate?"><meta property="og:image" content="{esc(image)}"><meta property="og:url" content="{esc(canonical)}">
<link rel="canonical" href="{esc(canonical)}">
<style>html,body{{margin:0;width:100%;height:100%;background:#111827}}iframe{{display:block;border:0;width:100%;height:100vh;height:100dvh}}a{{color:#cbe5ff}}</style>
</head><body>
<iframe src="{rel}x-player.html?p={esc(id)}" title="{esc(title)}" sandbox="allow-scripts allow-same-origin allow-popups allow-presentation"></iframe>
<noscript><a href="{rel}x-player.html?p={esc(id)}">Open the puzzle directly</a></noscript>
</body></html>
'''
    for p in records:(ROOT/'x-posts'/f'{p["id"]}.html').write_text(page(p),encoding='utf-8')
    (ROOT/'x-share.html').write_text(page(records[0],True),encoding='utf-8')
    groups=[]
    for n in range(1,7):
        links=''.join(f'<li><a href="x-posts/{p["id"]}.html">{p["id"]}</a> <span>{esc(p["source"]["game"])} ({p["source"]["year"]})</span></li>' for p in records if p['mate']==n)
        groups.append(f'<h2>Mate in {n}</h2><ul>{links}</ul>')
    (ROOT/'x-puzzles.html').write_text('<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Puzzle share links</title><style>body{font:16px system-ui;background:#111827;color:#eee;max-width:900px;margin:24px auto;padding:0 16px;line-height:1.6}a{color:#9bd1ff}li{margin:8px 0}span{color:#b9c5d7}</style><h1>Puzzle share links</h1><p>Post an individual link below on X. Each page has its own fixed starting puzzle and static Player Card metadata. The compact player has no engine picker or hints.</p>'+''.join(groups)+'<p><a href="PUZZLE_SOURCES.md">Position sources</a> &middot; <a href="X_PUZZLES_README.md">Setup instructions</a></p></html>',encoding='utf-8')
    print(f'Built {len(records)} fixed-puzzle cards for {base}')
    if not handle:print('No X handle supplied; twitter:site is omitted. Use --handle to add your real handle.')
if __name__=='__main__':main()

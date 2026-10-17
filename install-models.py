#!/usr/bin/env python3
"""Download Chess Teacher's local assets. Python 3.9+, standard library only.

Run in the application folder:
  Windows: py -3 install-models.py
  Linux/WSL: python3 install-models.py

This script writes only inside its own folder. It never uploads anything, edits
index.html, modifies a browser save, or installs system-wide packages.
Stockfish release assets are verified against upstream SHA-256 digests. Maia and
ORT are pinned together to one official frontend commit. Their downloaded hashes
are recorded locally; those records are not independent publisher signatures.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import sys
import time
import urllib.error
import urllib.request

ROOT = Path(__file__).resolve().parent
PIN = 'a6e52f5c811ee18863cb2f0e81f2433a5b9905de'
MAIA_BASE = f'https://raw.githubusercontent.com/CSSLab/maia-platform-frontend/{PIN}/'
STOCKFISH = 'https://github.com/nmrugg/stockfish.js/releases/download/v19.0.1/'
LOCKFILE = ROOT / 'download-lock.json'

# (path, URL, kind, optional upstream SHA-256)
BASE = [
 ('vendor/chess.js', 'https://cdn.jsdelivr.net/npm/chess.js@1.4.0/dist/esm/chess.js', 'chess', None),
 ('engine/stockfish-19-lite-single.js', STOCKFISH+'stockfish-19-lite-single.js', 'js', 'ccb130d7ff29408531c47d859a49f91d59d4f482d05a53eb1a3231a4f624c91a'),
 ('engine/stockfish-19-lite-single.wasm', STOCKFISH+'stockfish-19-lite-single.wasm', 'wasm', 'ee4f115bdb2d32cadf96cada104a05b5ec257d7ad6f57582190b49bc71f096de'),
]
FULL = [
 ('engine/stockfish-19-single.js', STOCKFISH+'stockfish-19-single.js', 'js', '8071dee87312f74805a859de933e1a1ef465579ab1a51fbd597388cdce9d444d'),
 ('engine/stockfish-19-single.wasm', STOCKFISH+'stockfish-19-single.wasm', 'wasm', '991bede2f253ebb08ff01fcc48270f4b9c8e66b12d5bd5f8d6f52eb3e3b3a740'),
]
MAIA = [
 ('models/maia3/maia3_simplified.onnx', MAIA_BASE+'public/maia3/maia3_simplified.onnx', 'model', None),
 ('models/maia3/all_moves.json', MAIA_BASE+'src/lib/engine/data/all_moves_maia3.json', 'mapping', None),
 ('vendor/ort/ort.wasm.min.js', MAIA_BASE+'public/ort/ort.wasm.min.js', 'ort', None),
 ('vendor/ort/ort-wasm-simd-threaded.mjs', MAIA_BASE+'public/ort/ort-wasm-simd-threaded.mjs', 'js', None),
 ('vendor/ort/ort-wasm-simd-threaded.wasm', MAIA_BASE+'public/ort/ort-wasm-simd-threaded.wasm', 'wasm', None),
]
LICENSES = [
 ('licenses/chess.js-LICENSE.txt', 'https://raw.githubusercontent.com/jhlywa/chess.js/v1.4.0/LICENSE', 'text', None),
 ('licenses/Stockfish-GPL-3.0.txt', 'https://raw.githubusercontent.com/nmrugg/stockfish.js/v19.0.1/Copying.txt', 'text', None),
 ('licenses/Maia-frontend-GPL-3.0.txt', MAIA_BASE+'LICENSE', 'text', None),
 ('licenses/Maia3-AGPL-3.0.txt', 'https://raw.githubusercontent.com/CSSLab/maia3/main/LICENSE', 'text', None),
 ('licenses/ONNX-Runtime-MIT.txt', 'https://raw.githubusercontent.com/microsoft/onnxruntime/v1.23.0/LICENSE', 'text', None),
 ('licenses/ONNX-Runtime-ThirdPartyNotices.txt', 'https://raw.githubusercontent.com/microsoft/onnxruntime/v1.23.0/ThirdPartyNotices.txt', 'text', None),
]

def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open('rb') as fh:
        for block in iter(lambda: fh.read(1024*1024), b''):
            h.update(block)
    return h.hexdigest()

def validate(path: Path, kind: str, expected: str | None = None) -> str:
    size = path.stat().st_size
    with path.open('rb') as fh:
        first = fh.read(1024)
    if size < 100:
        raise ValueError('File is unexpectedly short.')
    if first.lstrip().lower().startswith((b'<!doctype html', b'<html', b'<?xml')):
        raise ValueError('Got an HTML/error page, not the requested asset.')
    if first.startswith(b'version https://git-lfs'):
        raise ValueError('Got a Git LFS pointer rather than the binary file.')
    if kind == 'wasm' and first[:8] != b'\0asm\x01\0\0\0':
        raise ValueError('Invalid WebAssembly header.')
    if kind == 'model' and not 10_000_000 < size < 100_000_000:
        raise ValueError('Unexpected model size; expected the official 43.6 MiB Maia-3 browser export.')
    if kind == 'chess':
        text = path.read_text(encoding='utf-8')
        if not re.search(r'export\s*\{', text) or 'Chess' not in text:
            raise ValueError('chess.js is not the expected ES module.')
    if kind == 'ort' and b'ONNX Runtime Web v1.23.0' not in first:
        raise ValueError('The ONNX runtime is not the matching 1.23.0 build.')
    if kind == 'mapping':
        mapping = json.loads(path.read_text(encoding='utf-8'))
        if not isinstance(mapping, dict) or len(mapping) != 4352 or set(mapping.values()) != set(range(4352)):
            raise ValueError('Wrong Maia-3 move-index mapping.')
        for move in ['e2e4','e1g1','e1c1','a7a8q','a7a8n','a7b8r','h7g8b']:
            if move not in mapping:
                raise ValueError('Mapping is missing '+move)
    sha = digest(path)
    if expected and sha != expected:
        raise ValueError('SHA-256 does not match the published Stockfish release digest.')
    return sha

def download(item: tuple, lock: dict, check: bool, force: bool) -> None:
    rel, url, kind, expected = item
    dest = ROOT / rel
    prior = lock.get(rel, {})
    if dest.is_file() and not force:
        try:
            sha = validate(dest, kind, expected)
            if not expected and prior.get('url') == url and prior.get('sha256') and prior['sha256'] != sha:
                raise ValueError('File differs from the last recorded download. Use --force to replace it.')
            print('OK      '+rel)
            lock[rel] = {'url':url, 'sha256':sha, 'bytes':dest.stat().st_size, 'publisher_checksum':bool(expected)}
            return
        except (ValueError, OSError, UnicodeError, TypeError) as exc:
            if check:
                raise RuntimeError(f'{rel}: {exc}') from exc
            print(f'REPAIR  {rel}: {exc}')
    elif check:
        raise RuntimeError(f'Missing {rel}; run the installer without --check.')
    dest.parent.mkdir(parents=True, exist_ok=True)
    temp = dest.with_name(dest.name+'.part')
    for attempt in range(3):
        try:
            print('GET     '+rel, flush=True)
            request = urllib.request.Request(url, headers={'User-Agent':'ChessTeacherAssetInstaller/1.0', 'Accept-Encoding':'identity'})
            with urllib.request.urlopen(request, timeout=90) as response, temp.open('wb') as out:
                total = int(response.headers.get('Content-Length') or 0)
                got = 0
                report = time.monotonic()
                while True:
                    block = response.read(1024*1024)
                    if not block:
                        break
                    out.write(block)
                    got += len(block)
                    if got > 210*1024*1024:
                        raise ValueError('Unexpected asset larger than 210 MiB.')
                    if time.monotonic()-report > 2:
                        print(f'        {got/1048576:.1f} MiB'+(f' / {total/1048576:.1f} MiB' if total else ''), flush=True)
                        report = time.monotonic()
                if total and got != total:
                    raise ValueError('Download ended early.')
            sha = validate(temp, kind, expected)
            os.replace(temp, dest)
            lock[rel] = {'url':url, 'sha256':sha, 'bytes':dest.stat().st_size, 'publisher_checksum':bool(expected)}
            print(f'SAVED   {rel} ({dest.stat().st_size/1048576:.2f} MiB)')
            return
        except (OSError, ValueError, urllib.error.URLError) as exc:
            temp.unlink(missing_ok=True)
            if attempt == 2:
                raise RuntimeError(f'{rel}: {exc}') from exc
            print('        Retrying: '+str(exc), flush=True)
            time.sleep(attempt+1)

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--only', choices=['all','full','maia','lite'], default='all', help='Select optional assets; base assets and licences are always checked.')
    parser.add_argument('--check', action='store_true', help='Verify local files only, without internet access.')
    parser.add_argument('--force', action='store_true', help='Re-download assets, retaining old files until validation succeeds.')
    args = parser.parse_args()
    if args.check and args.force:
        parser.error('--check and --force cannot be combined')
    try:
        lock = json.loads(LOCKFILE.read_text()) if LOCKFILE.exists() else {}
        if not isinstance(lock, dict):
            lock = {}
    except (ValueError, OSError):
        lock = {}
    items = BASE + (FULL if args.only in ['all','full'] else []) + (MAIA if args.only in ['all','maia'] else []) + LICENSES
    errors=[]
    for item in items:
        try:
            download(item, lock, args.check, args.force)
        except Exception as exc:
            errors.append(str(exc)); print('ERROR   '+str(exc), file=sys.stderr)
        finally:
            # Retain completed downloads even if a later asset fails.
            if not args.check:
                tmp = LOCKFILE.with_suffix('.tmp')
                tmp.write_text(json.dumps(lock, indent=2)+'\n', encoding='utf-8')
                os.replace(tmp, LOCKFILE)
    if errors:
        print(f'\n{len(errors)} file(s) failed. Do not delete working engines. Fix the connection, then rerun.', file=sys.stderr)
        return 1
    print('\nAll selected files passed structural checks'+(' and recorded hash checks.' if args.check else '.'))
    print('Next: run py -3 -m http.server 8765 --bind 127.0.0.1 (Windows)')
    print('   or python3 -m http.server 8765 --bind 127.0.0.1 (WSL/Linux).')
    print('Open http://127.0.0.1:8765 and use the Engine dropdown.')
    print('No packages or runtime internet services are needed by the web app.')
    return 0

if __name__ == '__main__':
    raise SystemExit(main())

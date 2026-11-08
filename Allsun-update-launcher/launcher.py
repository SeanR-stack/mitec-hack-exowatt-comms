#!/usr/bin/env python3
"""allsun local version library. Python 3.9+, standard library only."""
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
from pathlib import Path
from urllib.parse import urlparse, parse_qs
import base64, hashlib, html, json, os, secrets, sys, tempfile, threading, webbrowser
ROOT = Path(__file__).resolve().parent
LOCK = threading.Lock()
TOKEN = secrets.token_urlsafe(32)
MAX_BYTES = 12 * 1024 * 1024

def library():
    return json.loads((ROOT / 'versions.json').read_text(encoding='utf-8'))

def save_json(value):
    tmp = ROOT / 'versions.json.tmp'
    tmp.write_text(json.dumps(value, indent=2), encoding='utf-8')
    os.replace(tmp, ROOT / 'versions.json')

class Handler(BaseHTTPRequestHandler):
    def log_message(self, *args): pass
    def respond(self, data, mime='application/json', status=200):
        if isinstance(data, str): data = data.encode('utf-8')
        self.send_response(status)
        self.send_header('Content-Type', mime)
        self.send_header('Content-Length', str(len(data)))
        self.send_header('Cache-Control', 'no-store')
        self.send_header('X-Content-Type-Options', 'nosniff')
        self.send_header('Referrer-Policy', 'no-referrer')
        self.end_headers()
        self.wfile.write(data)
    def host_ok(self):
        return self.headers.get('Host') == '127.0.0.1:' + str(self.server.server_port)
    def do_GET(self):
        if not self.host_ok(): return self.respond('Invalid host', 'text/plain', 403)
        u = urlparse(self.path)
        if u.path == '/':
            s=(ROOT / 'launcher.html').read_text(encoding='utf-8').replace('__TOKEN__', TOKEN)
            return self.respond(s, 'text/html; charset=utf-8')
        if u.path == '/api/versions': return self.respond(json.dumps(library()))
        if u.path == '/build':
            key = parse_qs(u.query).get('id', [''])[0]
            entry = next((x for x in library() if x['id'] == key), None)
            if not entry: return self.respond('Build not found', 'text/plain', 404)
            p = (ROOT / 'builds' / entry['file']).resolve()
            if p.parent != (ROOT / 'builds').resolve(): return self.respond('Invalid build path', 'text/plain', 403)
            return self.respond(p.read_bytes(), 'text/html; charset=utf-8')
        return self.respond('Not found', 'text/plain', 404)
    def do_POST(self):
        origin = 'http://127.0.0.1:' + str(self.server.server_port)
        if not self.host_ok() or self.headers.get('Origin') != origin or self.headers.get('X-allsun-Token') != TOKEN:
            return self.respond(json.dumps({'error':'Request not allowed'}), status=403)
        if self.path != '/api/import': return self.respond('{}', status=404)
        try:
            length = int(self.headers.get('Content-Length', '0'))
            if not 0 < length < MAX_BYTES * 1.4: raise ValueError('Update must be smaller than 12 MB.')
            data = json.loads(self.rfile.read(length))
            name = str(data.get('name', '')).strip()[:80]
            if not name: raise ValueError('Give this version a name.')
            raw = base64.b64decode(data['data'], validate=True)
            if not 0 < len(raw) <= MAX_BYTES: raise ValueError('Update must be smaller than 12 MB.')
            text = raw.decode('utf-8-sig')
            if '<html' not in text.lower() or '</html>' not in text.lower(): raise ValueError('Choose a complete standalone HTML build.')
            digest = hashlib.sha256(raw).hexdigest()
            with LOCK:
                rows = library()
                duplicate = next((x for x in rows if x['sha256'] == digest), None)
                if duplicate: return self.respond(json.dumps({'duplicate': True, 'entry': duplicate}))
                key = 'build-' + digest[:20]
                filename = key + '.html'
                target = ROOT / 'builds' / filename
                # New content-addressed filename: old builds are never overwritten.
                with target.open('xb') as f: f.write(raw)
                from datetime import datetime
                row = {'id':key,'name':name,'file':filename,'sha256':digest,'created':datetime.now().isoformat(timespec='seconds')}
                rows.insert(0, row)
                try: save_json(rows)
                except Exception:
                    target.unlink(missing_ok=True)
                    raise
            return self.respond(json.dumps({'duplicate':False,'entry':row}))
        except (ValueError, KeyError, UnicodeError) as e:
            return self.respond(json.dumps({'error':str(e)}), status=400)
        except Exception:
            return self.respond(json.dumps({'error':'Could not save the update. Check folder write access and free disk space.'}), status=500)

if __name__ == '__main__':
    server = ThreadingHTTPServer(('127.0.0.1', 0), Handler)
    url = 'http://127.0.0.1:' + str(server.server_port)
    print('allsun version library: ' + url, flush=True)
    print('Keep this window open. Press Ctrl+C to stop. Stored builds stay in this folder.', flush=True)
    if '--no-browser' not in sys.argv: webbrowser.open(url)
    try: server.serve_forever()
    except KeyboardInterrupt: pass
    finally: server.server_close()

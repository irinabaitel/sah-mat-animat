"""Verificare automată a paginilor: le deschide în Chrome fără fereastră și raportează erorile JavaScript
și fișierele care lipsesc (404).

Folosire (din rădăcina repo-ului):
    python tools/verifica_pagini.py                 # toate paginile .html din rădăcină
    python tools/verifica_pagini.py joc_*.html      # doar unele pagini
    python tools/verifica_pagini.py --minijocuri    # minijocurile, plus o partidă scurtă contra Robotului

La --minijocuri, fiecare joc e pornit cu ceas de 1 minut și (unde se poate) cu negrele, ca Robotul să mute primul.
Timpul e „virtual” (Chrome sare peste așteptări), deci câteva secunde de joc durează mult mai puțin.
Rulează după fiecare rundă mare de modificări, înainte de push.
"""
import sys, os, re, glob, subprocess, threading, http.server, socketserver, functools, io, urllib.parse

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PORT = 8765
CHROME = next((p for p in [r'C:\Program Files\Google\Chrome\Application\chrome.exe',
                           r'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe'] if os.path.exists(p)), None)
# mesaje care nu sunt greșeli ale noastre
IGNORE = re.compile(r'googletagmanager|google-analytics|gtag|favicon|ERR_INTERNET_DISCONNECTED|'
                    r'Permissions policy|DevTools|third-party cookie', re.I)

# pagina de test pentru minijocuri: încarcă jocul într-un iframe, alege ceas 1 min + negrele și pornește partida
RUNNER = """<!doctype html><meta charset="utf-8"><body><iframe id="f" style="width:1200px;height:900px"></iframe><script>
var page = decodeURIComponent(location.search.slice(1)), f = document.getElementById('f');
function log(m) { console.log('SMOKE ' + m); }
f.onload = function () {
  var w = f.contentWindow, d = f.contentDocument;
  w.addEventListener('error', function (e) { console.log('Uncaught (în joc) ' + e.message); });
  setTimeout(function () {
    try {
      var click = function (sel) { var el = d.querySelector(sel); if (el) el.click(); return !!el; };
      click('[data-secs="60"]');
      click('[data-color="black"]');
      var start = Array.prototype.slice.call(d.querySelectorAll('button')).filter(function (b) {
        return /Pornește|Începe|Start|Joacă/i.test(b.textContent) && b.offsetParent !== null; })[0];
      if (start) { start.click(); log('pornit: ' + start.textContent.trim().slice(0, 30)); } else log('fără buton de pornire');
    } catch (e) { console.log('Uncaught (test) ' + e.message); }
    setTimeout(function () {
      var st = d.querySelector('#status, #status-box, .status-box');
      log('stare după 20 s: ' + (st ? st.textContent.replace(/\\s+/g, ' ').trim().slice(0, 90) : '?'));
    }, 20000);
  }, 1500);
};
f.src = page;
</script>"""


class Quiet(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a): pass
    def do_GET(self):
        if self.path.startswith('/__runner'):
            b = RUNNER.encode('utf-8')
            self.send_response(200); self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.send_header('Content-Length', str(len(b))); self.end_headers(); self.wfile.write(b); return
        return super().do_GET()


def serve():
    socketserver.TCPServer.allow_reuse_address = True
    httpd = socketserver.ThreadingTCPServer(('127.0.0.1', PORT), functools.partial(Quiet, directory=ROOT))
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    return httpd


def run(url, budget):
    p = subprocess.run([CHROME, '--headless=new', '--disable-gpu', '--mute-audio', '--enable-logging=stderr', '--v=0',
                        '--virtual-time-budget=' + str(budget), '--window-size=1300,1000', '--dump-dom', url],
                       capture_output=True, timeout=180)
    err = p.stderr.decode('utf-8', 'replace')
    bad, smoke = [], []
    for line in err.splitlines():
        m = re.search(r'CONSOLE\(\d+\)\] "(.*)", source: (.*)$', line) or re.search(r':CONSOLE:\d+\] "(.*)", source: (.*)$', line)
        if not m: continue
        msg, src = m.group(1), m.group(2)
        if msg.startswith('SMOKE '): smoke.append(msg[6:]); continue
        if IGNORE.search(msg + ' ' + src): continue
        if 'Uncaught' in msg or 'Failed to load resource' in msg or 'Error' in msg:
            bad.append(msg + '  [' + re.sub(r'^http://127\.0\.0\.1:\d+/', '', src) + ']')
    return bad, smoke


def minigames():
    js = open(os.path.join(ROOT, 'minijocuri-nav.js'), encoding='utf-8').read()
    return sorted(set(re.findall(r"\['([a-z0-9_]+\.html)(?:\?[^']*)?'", js)))


def main():
    if not CHROME: print('Nu găsesc Chrome.'); return 2
    args = sys.argv[1:]
    mini = '--minijocuri' in args
    args = [a for a in args if a != '--minijocuri']
    os.chdir(ROOT)
    pages = minigames() if mini else sorted(set(sum([glob.glob(a) for a in args], [])) if args else glob.glob('*.html'))
    httpd = serve()
    total = 0
    for pg in pages:
        if mini: url, budget = 'http://127.0.0.1:%d/__runner?%s' % (PORT, urllib.parse.quote(pg)), 26000
        else:    url, budget = 'http://127.0.0.1:%d/%s' % (PORT, pg), 5000
        try:
            bad, smoke = run(url, budget)
        except subprocess.TimeoutExpired:
            bad, smoke = ['(nu s-a terminat în 3 minute)'], []
        total += len(bad)
        mark = 'OK ' if not bad else 'ERR'
        print(mark, pg, ('| ' + ' | '.join(smoke)) if smoke else '')
        for b in bad: print('     ', b[:300])
    httpd.shutdown()
    print('\n%d pagini, %d probleme' % (len(pages), total))
    return 1 if total else 0


if __name__ == '__main__':
    sys.exit(main())

import subprocess, threading, http.server, socketserver, os, re, sys
sys.stdout.reconfigure(encoding='utf-8')
ROOT=r'C:\Users\irina\SahMatAnimat'
class Q(http.server.SimpleHTTPRequestHandler):
    def __init__(s,*a,**k): super().__init__(*a,directory=ROOT,**k)
    def log_message(self,*a): pass
socketserver.TCPServer.allow_reuse_address=True
srv=socketserver.TCPServer(('127.0.0.1',8766),Q); threading.Thread(target=srv.serve_forever,daemon=True).start()
CH=r'C:\Program Files\Google\Chrome\Application\chrome.exe'
page=sys.argv[1] if len(sys.argv)>1 else '_test_l5.html'
r=subprocess.run([CH,'--headless=new','--disable-gpu','--autoplay-policy=no-user-gesture-required','--virtual-time-budget=180000','--window-size=1400,1000','--dump-dom','http://127.0.0.1:8766/'+page],capture_output=True,text=True,encoding='utf-8',timeout=300)
m=re.search(r'<pre id="out">(.*?)</pre>',r.stdout,re.S)
print(m.group(1) if m else r.stdout[-2000:]); srv.shutdown()

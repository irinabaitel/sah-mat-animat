import subprocess, threading, http.server, socketserver, sys
ROOT=r'C:\Users\irina\SahMatAnimat'; OUT=r'C:\Users\irina\AppData\Local\Temp\claude\5f5cca6ec2cb1060\c3522230-54fb-48d1-bcb0-1eb218f4609d\scratchpad\shots'
import os; os.makedirs(OUT,exist_ok=True)
class Q(http.server.SimpleHTTPRequestHandler):
    def __init__(s,*a,**k): super().__init__(*a,directory=ROOT,**k)
    def log_message(self,*a): pass
socketserver.TCPServer.allow_reuse_address=True
srv=socketserver.TCPServer(('127.0.0.1',8767),Q); threading.Thread(target=srv.serve_forever,daemon=True).start()
CH=r'C:\Program Files\Google\Chrome\Application\chrome.exe'
for s in sys.argv[1:]:
    subprocess.run([CH,'--headless=new','--disable-gpu','--hide-scrollbars','--virtual-time-budget=8000','--window-size=1280,760','--screenshot='+os.path.join(OUT,s+'.png'),'http://127.0.0.1:8767/_shot_l5.html?s='+s],capture_output=True,timeout=120)
srv.shutdown()

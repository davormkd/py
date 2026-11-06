from http.server import HTTPServer, BaseHTTPRequestHandler
import subprocess
import urllib.parse

class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urllib.parse.urlparse(self.path)
        if parsed_path.path == "/start":
            query = urllib.parse.parse_qs(parsed_path.query)
            win_path = query.get("path", ["."])[0]
            
            # Windows-Pfad (z.B. T:\...) in WSL-Pfad (/mnt/t/...) umwandeln
            try:
                wsl_path = subprocess.check_output(["wslpath", "-u", win_path], text=True).strip()
            except Exception:
                wsl_path = win_path

            print(empfaange Anforderung für Pfad: {wsl_path})

            # Startet ein neues interaktives Terminal (z.B. wt oder bash) auf dem Server
            # Hier wird der Agent mit dem konvertierten Pfad gestartet
            cmd = f"bash /home/gms24_ki/start_agent.sh '{wsl_path}'"
            
            # Öffnet ein neues Konsolenfenster auf dem Server (unter Windows/WSL)
            subprocess.Popen(["setsid", "bash", "/home/gms24_ki/start_agent.sh", wsl_path])
            
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"Agent auf Server gestartet!")
        else:
            self.send_response(404)
            self.end_headers()

run = lambda: HTTPServer(("0.0.0.0", 5000), SimpleHandler).serve_forever()
if __name__ == "__main__":
    print("HTTP-Trigger Server läuft auf Port 5000...")
    run()

from http.server import HTTPServer, BaseHTTPRequestHandler
import subprocess
import urllib.parse

class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urllib.parse.urlparse(self.path)
        if parsed_path.path == "/start":
            query = urllib.parse.parse_qs(parsed_path.query)
            path = query.get("path", ["."])[0]
            
            # Starte den Agenten im Hintergrund für diesen Pfad
            subprocess.Popen(["bash", "/home/gms24_ki/start_agent.sh", path])
            
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"Agent gestartet!")
        else:
            self.send_response(404)
            self.end_headers()

run = lambda: HTTPServer(("0.0.0.0", 5000), SimpleHandler).serve_forever()
if __name__ == "__main__":
    print("HTTP-Trigger Server laeuft auf Port 5000...")
    run()

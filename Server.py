import http.server
import socketserver

PORT = 8000

class GeoJSONCORSRequestHandler(http.server.SimpleHTTPRequestHandler):
    """Serve files with CORS headers and proper GeoJSON content type."""

    def end_headers(self):
        if self.path.endswith(".geojson"):
            # Send correct MIME type for GeoJSON files
            self.send_header("Content-Type", "application/geo+json")

        # Add CORS headers
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "X-Requested-With, Content-Type")

        super().end_headers()

# Use ThreadingHTTPServer to handle multiple requests concurrently
with http.server.ThreadingHTTPServer(("", PORT), GeoJSONCORSRequestHandler) as httpd:
    print(f"✅ Lokaler Server läuft auf http://localhost:{PORT}")
    httpd.serve_forever()

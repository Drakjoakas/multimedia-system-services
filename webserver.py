from http.server import BaseHTTPRequestHandler, HTTPServer
import execute_USB


VIDEO_TYPES = ['.mp4','.avi']
IMAGE_TYPES = ['.jpg','.jpeg','.png','.gif']
MUSIC_TYPES = ['.mp3']




class WebServer (BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        execute_USB.execute()
        self.wfile.write(bytes("YEY", "utf-8"))
        
        
def main(): 
    webServer = HTTPServer(("127.0.0.1", 5000), WebServer) 
    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass
    webServer.server_close()
    
if __name__ == "__main__":
    main()

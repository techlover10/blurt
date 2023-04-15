import gamestate
import connections

import multiprocessing

import http.server
import socketserver
import os

PORT = 8000

def serve_static():
    web_dir = os.path.join(os.path.dirname(__file__), '../static')
    os.chdir(web_dir)

    Handler = http.server.SimpleHTTPRequestHandler
    httpd = socketserver.TCPServer(("", PORT), Handler)
    print("serving static files at port", PORT)
    httpd.serve_forever()



def run():
    gs = gamestate.GameRunner(None, "data.db")
    cm = connections.ConnectionManager(gs.dispatch)
    gs.cm = cm
    cm.emptier = gs.emptier
    cm.leaver = gs.leaver
    cm.start_server()



if __name__ == "__main__":
    process = multiprocessing.Process(target=serve_static)
    process.start()
    run()

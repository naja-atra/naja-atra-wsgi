# -*- coding: utf-8 -*-
#


from naja_atra import route
from wsgiref.simple_server import WSGIServer, make_server
import naja_atra.server as server
import os
import signal


from threading import Thread

from naja_atra.utils.logger import get_logger, set_level
from naja_atra_wsgi import config, app


set_level("DEBUG")


_logger = get_logger("http_test")
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

wsgi_server: WSGIServer = None


@route("/stop")
def stop():
    global wsgi_server
    wsgi_server.shutdown()
    wsgi_server = None
    return "<!DOCTYPE html><html><head><title>关闭</title></head><body>关闭成功！</body></html>"


def start_server_wsgi():
    _logger.info("start server in background. ")
    server.scan(base_dir="tests/ctrls", regx=r'.*controllers.*')
    config(resources={"/public/*": f"{PROJECT_ROOT}/tests/static",
                    "/*": f"{PROJECT_ROOT}/tests/static"})

    global wsgi_server
    wsgi_server = make_server("", 9090, app)
    wsgi_server.serve_forever()


def on_sig_term(signum, frame):
    if wsgi_server:
        _logger.info(f"Receive signal [{signum}], shutdown the wsgi server...")
        Thread(target=wsgi_server.shutdown).start()


if __name__ == "__main__":
    signal.signal(signal.SIGTERM, on_sig_term)
    signal.signal(signal.SIGINT, on_sig_term)
    start_server_wsgi()

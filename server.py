# -*- coding: utf-8 -*-
import json
from threading import Thread
from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler


class JsonHandler(BaseHTTPRequestHandler):

    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        return

    # переопределяю логирование
    def log_message(self, format, *args):
        return

    def do_GET(self):
        self._set_headers()
    # processing request
        return

    def do_HEAD(self):
        self._set_headers()
        return

    @staticmethod
    def check_json(request):
        try:
            json.loads(request)
        except ValueError:
            return False
        return True

    def do_POST(self):
        self._set_headers()
        content_len = int(self.headers.getheader('Content-Length', 0))
        body = self.rfile.read(content_len)
        # проверяем json на валидность
        check = self.check_json(body)
        #       processing request
        # for write use:
        # self.wfile.write('{"ok" : "ok"}')
        return


class MultiThreadHTTPServer(HTTPServer):
    def process_request(self, request, client_address):
        thread = Thread(target=self.__new_request, args=(self.RequestHandlerClass, request, client_address, self))
        thread.start()

    def __new_request(self, handlerclass, request, address, server):
        handlerclass(request, address, server)
        self.shutdown_request(request)


class HttpGate():
    @staticmethod
    def http_gate():
        httpd = MultiThreadHTTPServer(('', 20756), JsonHandler)
        httpd.serve_forever()

HttpGate().http_gate()

import json
import logging
import os
import ssl
import time
from logging.handlers import RotatingFileHandler

import tornado.httpserver
import tornado.ioloop
import tornado.locks
import tornado.web
import tornado.routing
from tornado.options import define, options

from system.oracle import create_pool, DB_CONFIG
import routes

tornado.log.enable_pretty_logging()
tornado.options.parse_command_line()


define("dev", default=True, help="dev or prod", type=bool)
define("port", default=12345, help="run on the given port", type=int)


class Application(tornado.web.Application):
    def __init__(self, pool):
        self.pool = pool

        settings = dict(
            log_function=self.log_function
        )
        self.set_logger("tornado.access", "access.log")
        self.set_logger("tornado.application", "app.log")
        self.set_logger("tornado.general", "general.log")
        super(Application, self).__init__(routes.handlers, **settings)

    def log_function(self, handler):
        t = time.localtime()
        log = {
            'datetime': time.asctime(t),
            'status_code': handler.get_status(),
            'method': handler.request.method,
            'URL': handler.request.uri,
            'remote_ip': handler.request.remote_ip,
            'user_agent': handler.request.headers.get('User-agent'),
            'elapsed_time_ms': '%.2f' % (handler.request.request_time()*1000)
        }
        if handler.get_status() < 400:
            log_method = tornado.log.access_log.info
        elif handler.get_status() < 500:
            log_method = tornado.log.access_log.warning
        else:
            log_method = tornado.log.access_log.error

        log_method(json.dumps(log, indent=4))

    def set_logger(self, logger_name, file_name, level=logging.INFO,
                   maxBytes=1000000, backupCount=10):
        logger = logging.getLogger(logger_name)
        logger.setLevel(level)
        fh = RotatingFileHandler(os.path.join("log", file_name),
                                 maxBytes=maxBytes,
                                 backupCount=backupCount)
        logger.addHandler(fh)


async def main():
    pool = await create_pool(tornado.ioloop.IOLoop.current(), **DB_CONFIG)
    ssl_ctx = None
    if not options.dev:
        ssl_ctx = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        ssl_ctx.load_cert_chain(os.path.join("certs", "shiva_ws.crt"),
                                os.path.join("certs", "shiva_ws.crt"))
    app = Application(pool)

    http_server = tornado.httpserver.HTTPServer(
        app, ssl_options=ssl_ctx, xheaders=True)
    http_server.listen(options.port)
    await shutdown_event.wait()

if __name__ == "__main__":
    try:
        shutdown_event = tornado.locks.Event()
        tornado.ioloop.IOLoop.current().run_sync(main)
    except KeyboardInterrupt:
        print("shutdown")
        shutdown_event.set()

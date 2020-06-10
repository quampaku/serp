import json
from typing import (
    Any,
    Awaitable,
    Dict,
    Optional,
    Tuple
)

import traceback

import tornado.web

from services.address_book import AddressBookService


def log_function(handler: tornado.web.RequestHandler) -> None:
    status = handler.get_status()
    request_time = 1000.0 * handler.request.request_time()

    msg = 'RESPONSE: {status} {method} {uri} ({ip} {time}ms)'.format(
        status=status,
        method=handler.request.method,
        uri=handler.request.uri,
        ip=handler.request.remote_ip,
        time=request_time
    )

    print(msg)

def make_app(
    config: Dict,
    debug: bool
) -> Tuple[]
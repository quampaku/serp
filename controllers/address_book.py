import json

import tornado.web

from controllers.base import BaseRequestHandler

ADDRESSBOOK_ENTRY_URI_FORMAT_STR = r'/addresses/{id}'


class AddressBookRequestHandler(BaseRequestHandler):
    async def get(self):
        all_addrs = await self.service.get_all_addresses()
        self.set_status(200)
        self.finish(all_addrs)

    async def post(self):
        try:
            addr = json.loads(self.request.body.decode('utf-8'))
            id = await self.service.create_address(addr)
            addr_uri = ADDRESSBOOK_ENTRY_URI_FORMAT_STR.format(id=id)
            self.set_status(201)
            self.set_header('Location', addr_uri)
            self.finish()
        except (json.decoder.JSONDecodeError, TypeError):
            raise tornado.web.HTTPError(
                400, reason='Invalid JSON body'
            )
        except ValueError as e:
            raise tornado.web.HTTPError(400, reason=str(e))

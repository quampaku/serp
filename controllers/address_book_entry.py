import json

import tornado.web

from controllers.base import BaseRequestHandler


class AddressBookEntryRequestHandler(BaseRequestHandler):
    async def get(self, id):
        try:
            addr = await self.service.get_address(id)
            self.set_status(200)
            self.finish(addr)
        except KeyError as e:
            raise tornado.web.HTTPError(404, reason=str(e))

    async def put(self, id):
        try:
            addr = json.loads(self.request.body.decode('utf-8'))
            await self.service.update_address(id, addr)
            self.set_status(204)
            self.finish()
        except (json.decoder.JSONDecodeError, TypeError):
            raise tornado.web.HTTPError(
                400, reason='Invalid JSON body'
            )
        except KeyError as e:
            raise tornado.web.HTTPError(404, reason=str(e))
        except ValueError as e:
            raise tornado.web.HTTPError(400, reason=str(e))

    async def delete(self, id):
        try:
            await self.service.delete_address(id)
            self.set_status(204)
            self.finish()
        except KeyError as e:
            raise tornado.web.HTTPError(404, reason=str(e))

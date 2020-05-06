from system.base_handler import BaseHandler


class RegisterHandler(BaseHandler):
    async def get(self):
        self.render("views/register.html")

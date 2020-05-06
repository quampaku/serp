from controllers.main import MainHandler
from controllers.register import RegisterHandler


handlers = [
    (r"/", MainHandler),
    (r"/main/register", RegisterHandler)
]

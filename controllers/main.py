from system.base_handler import BaseHandler


class MainHandler(BaseHandler):
    async def get(self):
        self.render("views/index.html")
        # async def body(cur):
        #     await cur.execute("select * from test.cp_emp where id = " + str(i))
        #     rows = await cur.fetchmany()
        #     print(rows)

        # for i in range(5):
        #     print(i)
        #     async with await self.pool.acquire() as conn:
        #         async with await conn.cursor() as cursor:
        #             await body(cursor)
        #     await tornado.gen.sleep(1)

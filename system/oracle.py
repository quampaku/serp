from functools import partial

import cx_Oracle


DB_CONFIG = dict(
    host="192.168.0.160",
    port=1521,
    sid="FEO",
    user="test",
    password="test",
    min_sessions=1,
    max_sessions=1,
    inc_sessions=0,
    threaded=True,
    encoding="utf-8"
)


class Pool:
    def __init__(self, ioloop, **DB_CONFIG):
        self._ioloop = ioloop
        self.db_config = DB_CONFIG
        pass

    def __await__(self):
        return self._init().__await__()

    async def _init(self):
        self._pool = await self._ioloop.run_in_executor(
            None,
            partial(cx_Oracle.SessionPool,
                    user=self.db_config['user'],
                    password=self.db_config['password'],
                    dsn=cx_Oracle.makedsn(
                        self.db_config['host'],
                        self.db_config['port'],
                        self.db_config['sid']),
                    min=self.db_config['min_sessions'],
                    max=self.db_config['max_sessions'],
                    increment=self.db_config['inc_sessions'],
                    threaded=self.db_config['threaded'],
                    encoding=self.db_config['encoding'])
        )
        return self

    def acquire(self, *, timeout=None):
        return PoolAcquireContext(self, timeout)

    async def _acquire(self, timeout):
        conn = await self._ioloop.run_in_executor(None, self._pool.acquire)
        return Connection(self._ioloop, conn)

    async def release(self, conn):
        await self._ioloop.run_in_executor(None, self._pool.release, conn)


class PoolAcquireContext:
    __slots__ = ('timeout', 'connection', 'done', 'pool')

    def __init__(self, pool, timeout):
        self.pool = pool
        self.timeout = timeout
        self.connection = None
        self.done = False

    async def _acquire(self):
        if self.connection is not None or self.done:
            raise cx_Oracle.InterfaceError('a connection is already acquired')
        return await self.pool._acquire(self.timeout)

    async def __aenter__(self):
        self.connection = await self._acquire()
        return self.connection

    async def __aexit__(self, *exc):
        self.done = True
        con = self.connection
        self.connection = None
        await self.pool.release(con._conn)

    def __await__(self):
        self.done = True
        return self.pool._acquire(self.timeout).__await__()


class Cursor:
    def __init__(self, ioloop, cursor):
        self._ioloop = ioloop
        self._cursor = cursor

    async def execute(self, *args, **kargs):
        return await self._ioloop.run_in_executor(
            None,
            partial(self._cursor.execute,
                    *args, **kargs)
        )

    async def executemany(self, *args, **kargs):
        return await self._ioloop.run_in_executor(
            None,
            partial(self._cursor.executemany,
                    *args, **kargs)
        )

    async def fetchmany(self, *args, **kargs):
        return await self._ioloop.run_in_executor(
            None,
            partial(self._cursor.fetchmany,
                    *args, **kargs)
        )

    async def fetchall(self, *args, **kargs):
        return await self._ioloop.run_in_executor(
            None,
            partial(self._cursor.fetchall,
                    *args, **kargs)
        )

    async def setinputsizes(self, *args, **kargs):
        return await self._ioloop.run_in_executor(
            None,
            partial(self._cursor.setinputsizes,
                    *args, **kargs)
        )

    async def var(self, *args, **kargs):
        return await self._ioloop.run_in_executor(
            None,
            partial(self._cursor.var,
                    *args, **kargs)
        )

    async def fetchone(self):
        return self._cursor.fetchone()

    def description(self):
        return self._cursor.description()

    def rowcount(self):
        return self._cursor.rowcount

    async def __aenter__(self):
        return self

    async def __aexit__(self, *exc):
        self.done = True
        await self._ioloop.run_in_executor(None, self._cursor.close)
        print("conn close")


class Connection:
    def __init__(self, ioloop, conn):
        self._conn = conn
        self._ioloop = ioloop
        return

    async def cursor(self):
        return Cursor(self._ioloop,
                      await self._ioloop.run_in_executor(
                          None,
                          self._conn.cursor))

    async def commit(self):
        return Cursor(self._ioloop,
                      await self._ioloop.run_in_executor(
                          None,
                          self._conn.commit))

    async def close(self):
        return Cursor(self._ioloop,
                      await self._ioloop.run_in_executor(
                          None,
                          self._conn.close))

    async def ltxid(self):
        return Cursor(self._ioloop,
                      await self._ioloop.run_in_executor(
                          None,
                          self._conn.ltxid))

    async def __aenter__(self):
        return self

    async def __aexit__(self, *exc):
        self.done = True
        await self._ioloop.run_in_executor(None, self._conn.close)
        print("cursor close")


def create_pool(ioloop, **DB_CONFIG):
    return Pool(ioloop, **DB_CONFIG)

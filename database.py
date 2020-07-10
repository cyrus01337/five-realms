"""
Async database wrapper
"""
import aiosqlite

# import errors
from player import Player

FILENAME = "DATABASE.db"


class Database(object):
    def requires_conn(coroutine):
        async def predicate(self, *args, **kwargs):
            async with aiosqlite.connect(FILENAME) as conn:
                ret = await coroutine(self, conn, *args, **kwargs)
                await conn.commit()

                if ret is not None:
                    return ret
        return predicate

    def __init__(self, loop):
        self.loop = loop
        self._tables = (
            """
                CREATE TABLE IF NOT EXISTS users(
                    id int NOT NULL,
                    realm varchar(6) NOT NULL,
                    race varchar(12),
                    level int,
                    exp int,
                    class_type varchar(7)
                );
            """,

            """
                CREATE TABLE IF NOT EXISTS stats(
                    id int NOT NULL,
                    health int NOT NULL,
                    strength decimal NOT NULL
                );
            """
        )

        self.loop.create_task(self.__ainit__())

    @requires_conn
    async def __ainit__(self, conn):
        for query in self._tables:
            await conn.execute(query)
        await conn.commit()

    @requires_conn
    async def insert(self, conn, *params, **kwargs):
        params += tuple(kwargs.values())
        inserting = (", ").join("?" for _ in params)
        query = f"INSERT INTO users VALUES({inserting});"

        await conn.execute(query, params)

    @requires_conn
    async def remove(self, conn, user_id: int):
        query = "DELETE FROM users WHERE id=?;"
        params = (
            user_id,
        )

        await conn.execute(query, params)
        await conn.commit()

    @requires_conn
    async def update(self, conn, user_id: int, **params):
        setting = ""
        keys = params.keys()
        values = params.values()
        irange = range(len(keys))

        for i, k, v in zip(irange, keys, values):
            i += 1
            append = ""

            if i < len(irange):
                append += ", "

            if isinstance(v, str):
                v = repr(v)
            setting += f"{k}={v}{append}"
        query = f"UPDATE users SET {setting} WHERE id=?;"
        params = (
            user_id,
        )

        await conn.execute(query, params)

    @requires_conn
    async def clear(self, conn):
        await conn.execute("DELETE FROM users;")

    @requires_conn
    async def get(self, conn):
        async with conn.execute("SELECT * FROM users;") as cursor:
            return await cursor.fetchall()

    @requires_conn
    async def get_player(self, conn, user_id: int):
        query = "SELECT * FROM users WHERE id=?;"
        params = (
            user_id,
        )

        async with conn.execute(query, params) as cursor:
            args = await cursor.fetchone()

            # if data equals nothing, return nothing
            if args is None:
                return args
            return Player(*args)

    @requires_conn
    async def save(self, conn, player: Player):
        await self.update(player.id, **player.get_changes())


async def create(loop):
    return Database(loop)

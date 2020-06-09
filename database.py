"""
Async database wrapper
"""
import os

import aiosqlite

# import errors
from player import Player

filename = "DATABASE.db"


async def init():
    if os.path.exists(filename) is False:
        async with aiosqlite.connect(filename) as db:
            await db.execute("""
                CREATE TABLE users(
                    ID int NOT NULL,
                    Realm varchar(6) NOT NULL
                );
            """)
            await db.commit()
    return await get()


async def get():
    async with aiosqlite.connect(filename) as db:
        async with db.execute("SELECT * FROM users;") as cursor:
            return await cursor.fetchall()


async def get_user(user_id: int):
    async with aiosqlite.connect(filename) as db:
        query = "SELECT * FROM users WHERE id=?;"
        params = (
            user_id,
        )

        async with db.execute(query, params) as cursor:
            args = await cursor.fetchone()

            if args is None:
                return args
            return Player(*args)


async def insert(*params, **kwargs):
    params += tuple(kwargs.values())

    async with aiosqlite.connect(filename) as db:
        inserting = (", ").join("?" for _ in params)
        await db.execute(f"INSERT INTO users VALUES({inserting});", params)
        await db.commit()


async def remove(user_id: int):
    async with aiosqlite.connect(filename) as db:
        await db.execute("DELETE FROM users WHERE id=?;", (user_id,))
        await db.commit()


async def update(user_id: int, **params):
    async with aiosqlite.connect(filename) as db:
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
        params = (
            user_id,
        )
        await db.execute(f"UPDATE users SET {setting} WHERE id=?;", params)
        await db.commit()


async def clear():
    async with aiosqlite.connect(filename) as db:
        await db.execute("DELETE FROM users;")
        await db.commit()


async def save(cache):
    async with aiosqlite.connect(filename) as db:
        return db


async def close():
    async with aiosqlite.connect(filename) as db:
        await db.close()

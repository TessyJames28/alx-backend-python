import aiosqlite
import asyncio
import os

# Get absolute path to users.db from the current file
db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'python-decorators-0x01', 'users.db'))


async def async_fetch_users():
    """Async function to fetch all users"""
    async with aiosqlite.connect(db_path) as db:
        cursor = await db.execute("SELECT * FROM users")
        users = await cursor.fetchall()
        print(users)


async def async_fetch_older_users():
    """Async function to fetch older users"""
    async with aiosqlite.connect(db_path) as db:
        cursor = await db.execute("SELECT * FROM users WHERE age > 110")
        older_users = await cursor.fetchall()
        print(older_users)
    

async def main():
    await asyncio.gather(
        async_fetch_users(),
        async_fetch_older_users(),
    )

asyncio.run(main())

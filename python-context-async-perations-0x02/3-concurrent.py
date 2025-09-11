import sqlite3
import asyncio
import aiosqlite


#### Run multiple database queries concurrently using asyncio.gather.

#### Async function to fetch all users
async def async_fetch_users():
    async with aiosqlite.connect('users.db') as conn:
        cursor = await conn.execute("SELECT * FROM users")
        users = await cursor.fetchall()
        await cursor.close()
        return users
    
#### Async function to fetch users older than 40
async def async_fetch_older_users():
    async with aiosqlite.connect('users.db') as conn:
        cursor = await conn.execute("SELECT * FROM users WHERE age > ?", (40,))
        older_users = await cursor.fetchall()
        await cursor.close()
        return older_users
    
#### Main async function to run both queries concurrently
async def fetch_concurrently():
    users_task = async_fetch_users()
    older_users_task = async_fetch_older_users()
    
    users, older_users = await asyncio.gather(users_task, older_users_task)
    
    print("All Users:", users)
    print("Users Older than 40:", older_users)

asyncio.run(fetch_concurrently())
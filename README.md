# basic async wrapper for aiosql
example code:
```py
import aiosqlite_wrapper as aiosqlite
import asyncio # only used to run async function

async def main():
    # define a database instance
    db = aiosqlite.database("database.sqlite")
    # execute a query
    await db.execute('create table test(foo text)')

asyncio.run(main())
```
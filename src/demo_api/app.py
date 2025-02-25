from fastapi import FastAPI
import os
from sqlalchemy.ext.asyncio import create_async_engine

DATABASE_URL = os.getenv("SERVER_DATABASE_CONNECTION_URL")

app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "Hello, World!"}


async def check_db_connection():
    try:
        engine = create_async_engine(DATABASE_URL)
        async with engine.connect() as conn:
            if conn:
                return {"status": "connected"}
            else:
                return {"status": "error", "details": "Invalid connection"}
    except Exception as e:
        return {"status": "error", "details": str(e)}


@app.get("/db-status")
async def get_db_status():
    return await check_db_connection()

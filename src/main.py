import os
from .demo_api.app import app


SERVER_API_HOST = os.getenv("SERVER_API_HOST")
SERVER_API_PORT = int(os.getenv("SERVER_API_PORT"))

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host=SERVER_API_HOST, port=SERVER_API_PORT)

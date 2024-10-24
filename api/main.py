from fastapi import FastAPI
from api.middlewares import AdvancedMiddleware


app = FastAPI()


app.add_middleware(AdvancedMiddleware)


@app.get("/")
async def main():
    return {"message": "Helo India !"}

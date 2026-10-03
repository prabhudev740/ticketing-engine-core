from contextlib import asynccontextmanager
from fastapi import FastAPI
import uvicorn
from app.utils.helpers import verify_path_exists
from app.core.logging_conf import Logger


@asynccontextmanager
async def lifespan(app: FastAPI):
    verify_path_exists('logs/')
    # await create_db_and_tables()
    log.info("Database tables verified/created and startup tasks completed.")
    yield
    log.info("Shutting down API Gateway...")

log = Logger.log(__name__)
app = FastAPI(title="Ticketing Engine - API Gateway", lifespan=lifespan)

@app.get("/")
async def root():
    log.info("status called")
    return {"status": "OK"}

def main():
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)

if __name__ == "__main__":
    main()

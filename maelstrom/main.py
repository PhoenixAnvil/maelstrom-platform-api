from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from maelstrom.db import Base, engine
from maelstrom.routes import product

app = FastAPI(title="Maelstrom API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


app.include_router(product.router)

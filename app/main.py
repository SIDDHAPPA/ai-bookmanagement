from fastapi import FastAPI
from app.routes import books, ai, recommendations, auth
from app.database import engine, Base

app = FastAPI(title="AI Book Management System")

app.include_router(auth.router)
app.include_router(books.router)
app.include_router(recommendations.router)
app.include_router(ai.router)

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

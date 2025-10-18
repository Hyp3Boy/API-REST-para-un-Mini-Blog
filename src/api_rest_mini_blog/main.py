from fastapi import FastAPI
from api_rest_mini_blog.database import Base, engine
from api_rest_mini_blog.routers import users, posts 

app = FastAPI(
    title="API para un Mini-Blog",
    description="Una API REST para gestionar usuarios, posts y comentarios.",
    version="0.1.0"
)

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

app.include_router(users.router)
app.include_router(posts.router)

@app.get("/", tags=["Root"])
def read_root():
    return {"message": "Bienvenido a la API del Mini-Blog"}
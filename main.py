from fastapi import FastAPI
from routers.movies_router import router as movies_router
from routers.comments_router import router as comments_router
from routers.actors_router import router as actors_router

app = FastAPI()

for router in [movies_router, comments_router, actors_router]:
    app.include_router(router)

@app.get("/")
async def root():
    return {"message": "Server is running"}
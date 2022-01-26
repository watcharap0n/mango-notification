from routers import api
from fastapi import FastAPI, Depends, HTTPException, status


app = FastAPI()

app.include_router(
    api.router,
    prefix="/api/line/post/card"
)

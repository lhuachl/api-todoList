
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(
    title="TODO App API",
    description="Una API simple para gestionar tareas TODO",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Importar   y registrar routers
from routers.user import router as user_router
from routers.task import router as task_router

app.include_router(user_router, prefix="/users", tags=["Usuarios"])
app.include_router(task_router, prefix="/tasks", tags=["Tareas"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

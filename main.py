from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from supabase import create_client, Client
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Configuración de Supabase
SUPABASE_URL = os.getenv("SUPABASE_URL", "")
SUPABASE_KEY = os.getenv("SUPABASE_ANON_KEY", "")

# Crear cliente de Supabase
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

app = FastAPI(
    title="TODO App API",
    description="Una API simple para gestionar tareas TODO",
    version="1.0.0"
)

# Configuración de CORS para permitir peticiones desde Razor (.NET) u otros frontends
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Cambia esto por el dominio de tu frontend en producción
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Modelos Pydantic
class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    status: str = "To Do"
    priority: int = 1

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    priority: Optional[int] = None

class Task(BaseModel):
    id: int
    title: str
    description: Optional[str]
    status: str
    priority: int
    created_at: datetime
    updated_at: datetime

# Endpoints
@app.get("/")
async def root():
    """Endpoint raíz de la API"""
    return {"message": "Bienvenido a la TODO App API"}

@app.get("/health")
async def health_check():
    """Verificar el estado de la API"""
    return {"status": "healthy", "timestamp": datetime.now()}

@app.post("/tasks/", response_model=Task, status_code=status.HTTP_201_CREATED)
async def create_task(task: TaskCreate):
    """Crear una nueva tarea"""
    try:
        # Insertar tarea en Supabase
        result = supabase.table("tasks").insert({
            "title": task.title,
            "description": task.description,
            "status": task.status,
            "priority": task.priority
        }).execute()
        
        if result.data:
            return result.data[0]
        else:
            raise HTTPException(status_code=400, detail="Error al crear la tarea")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")

@app.get("/tasks/", response_model=List[Task])
async def get_tasks(status_filter: Optional[str] = None, priority_filter: Optional[int] = None):
    """Obtener todas las tareas con filtros opcionales"""
    try:
        query = supabase.table("tasks").select("*")
        
        # Aplicar filtros si están presentes
        if status_filter:
            query = query.eq("status", status_filter)
        if priority_filter:
            query = query.eq("priority", priority_filter)
        
        result = query.order("created_at", desc=True).execute()
        return result.data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener las tareas: {str(e)}")

@app.get("/tasks/{task_id}", response_model=Task)
async def get_task(task_id: int):
    """Obtener una tarea específica por ID"""
    try:
        result = supabase.table("tasks").select("*").eq("id", task_id).execute()
        
        if not result.data:
            raise HTTPException(status_code=404, detail="Tarea no encontrada")
        
        return result.data[0]
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener la tarea: {str(e)}")

@app.put("/tasks/{task_id}", response_model=Task)
async def update_task(task_id: int, task_update: TaskUpdate):
    """Actualizar una tarea existente"""
    try:
        # Verificar que la tarea existe
        existing_task = supabase.table("tasks").select("*").eq("id", task_id).execute()
        if not existing_task.data:
            raise HTTPException(status_code=404, detail="Tarea no encontrada")
        
        # Preparar datos para actualizar
        update_data = {}
        if task_update.title is not None:
            update_data["title"] = task_update.title
        if task_update.description is not None:
            update_data["description"] = task_update.description
        if task_update.status is not None:
            update_data["status"] = task_update.status
        if task_update.priority is not None:
            update_data["priority"] = task_update.priority
        
        update_data["updated_at"] = datetime.now().isoformat()
        
        # Actualizar en Supabase
        result = supabase.table("tasks").update(update_data).eq("id", task_id).execute()
        
        if result.data:
            return result.data[0]
        else:
            raise HTTPException(status_code=400, detail="Error al actualizar la tarea")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al actualizar la tarea: {str(e)}")

@app.delete("/tasks/{task_id}")
async def delete_task(task_id: int):
    """Eliminar una tarea"""
    try:
        # Verificar que la tarea existe
        existing_task = supabase.table("tasks").select("*").eq("id", task_id).execute()
        if not existing_task.data:
            raise HTTPException(status_code=404, detail="Tarea no encontrada")
        
        # Eliminar la tarea
        result = supabase.table("tasks").delete().eq("id", task_id).execute()
        
        return {"message": "Tarea eliminada exitosamente", "task_id": task_id}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al eliminar la tarea: {str(e)}")

@app.get("/tasks/status/{status}")
async def get_tasks_by_status(status: str):
    """Obtener tareas por estado específico"""
    try:
        result = supabase.table("tasks").select("*").eq("status", status).order("created_at", desc=True).execute()
        return {"status": status, "tasks": result.data, "count": len(result.data)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener tareas por estado: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

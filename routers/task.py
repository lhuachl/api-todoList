from fastapi import APIRouter, HTTPException, status
from typing import List, Optional
import os
from supabase import create_client, Client
from dotenv import load_dotenv
from models.task import TaskCreate, TaskUpdate, Task

load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL", "")
SUPABASE_KEY = os.getenv("SUPABASE_ANON_KEY", "")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

router = APIRouter()

@router.post("/", response_model=Task, status_code=status.HTTP_201_CREATED)
async def create_task(task: TaskCreate):
	"""Crear una nueva tarea asociada a un usuario"""
	try:
		user = supabase.table("users").select("*").eq("id", task.user_id).execute()
		if not user.data:
			raise HTTPException(status_code=404, detail="Usuario no encontrado")
		result = supabase.table("tasks").insert({
			"user_id": task.user_id,
			"title": task.title,
			"description": task.description if task.description is not None else None,
			"status": task.status if task.status is not None else "To Do",
			"priority": task.priority if task.priority is not None else 1
		}).execute()
		if result.data:
			data = result.data[0]
			if "description" not in data:
				data["description"] = None
			return data
		else:
			raise HTTPException(status_code=400, detail="Error al crear la tarea")
	except Exception as e:
		raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")

@router.get("/", response_model=List[Task])
async def get_tasks(user_id: Optional[int] = None, status_filter: Optional[str] = None, priority: Optional[int] = None):
	"""Obtener tareas, opcionalmente filtradas por usuario, estado y prioridad"""
	try:
		query = supabase.table("tasks").select("*")
		if user_id:
			query = query.eq("user_id", user_id)
		if status_filter:
			query = query.eq("status", status_filter)
		if priority:
			query = query.eq("priority", priority)
		result = query.order("created_at", desc=True).execute()
		tasks = result.data
		for t in tasks:
			if "description" not in t:
				t["description"] = None
		return tasks
	except Exception as e:
		raise HTTPException(status_code=500, detail=f"Error al obtener las tareas: {str(e)}")

@router.get("/{task_id}", response_model=Task)
async def get_task(task_id: int):
	"""Obtener una tarea específica por ID"""
	try:
		result = supabase.table("tasks").select("*").eq("id", task_id).execute()
		if not result.data:
			raise HTTPException(status_code=404, detail="Tarea no encontrada")
		data = result.data[0]
		if "description" not in data:
			data["description"] = None
		return data
	except Exception as e:
		raise HTTPException(status_code=500, detail=f"Error al obtener la tarea: {str(e)}")

@router.put("/{task_id}", response_model=Task)
async def update_task(task_id: int, task_update: TaskUpdate):
	"""Actualizar una tarea existente"""
	try:
		existing_task = supabase.table("tasks").select("*").eq("id", task_id).execute()
		if not existing_task.data:
			raise HTTPException(status_code=404, detail="Tarea no encontrada")
		update_data = {}
		if task_update.title is not None:
			update_data["title"] = task_update.title
		if task_update.description is not None:
			update_data["description"] = task_update.description
		if task_update.status is not None:
			update_data["status"] = task_update.status
		if task_update.priority is not None:
			update_data["priority"] = task_update.priority
		update_data["updated_at"] = existing_task.data[0]["updated_at"]
		result = supabase.table("tasks").update(update_data).eq("id", task_id).execute()
		if result.data:
			return result.data[0]
		else:
			raise HTTPException(status_code=400, detail="Error al actualizar la tarea")
	except Exception as e:
		raise HTTPException(status_code=500, detail=f"Error al actualizar la tarea: {str(e)}")

@router.delete("/{task_id}")
async def delete_task(task_id: int):
	"""Eliminar una tarea"""
	try:
		existing_task = supabase.table("tasks").select("*").eq("id", task_id).execute()
		if not existing_task.data:
			raise HTTPException(status_code=404, detail="Tarea no encontrada")
		supabase.table("tasks").delete().eq("id", task_id).execute()
		return {"message": "Tarea eliminada exitosamente", "task_id": task_id}
	except Exception as e:
		raise HTTPException(status_code=500, detail=f"Error al eliminar la tarea: {str(e)}")

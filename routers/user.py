from fastapi import APIRouter, HTTPException, status
from typing import List
import os
from supabase import create_client, Client
from dotenv import load_dotenv
from models.user import UserCreate, User

load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL", "")
SUPABASE_KEY = os.getenv("SUPABASE_ANON_KEY", "")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

router = APIRouter()

@router.post("/", response_model=User, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate):
	"""Crear un nuevo usuario"""
	try:
		result = supabase.table("users").insert({"username": user.username}).execute()
		if result.data:
			return result.data[0]
		else:
			raise HTTPException(status_code=400, detail="Error al crear el usuario")
	except Exception as e:
		raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")

@router.get("/", response_model=List[User])
async def get_users():
	"""Obtener todos los usuarios"""
	try:
		result = supabase.table("users").select("*").execute()
		return result.data
	except Exception as e:
		raise HTTPException(status_code=500, detail=f"Error al obtener usuarios: {str(e)}")

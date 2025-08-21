# TODO App API

Una API REST simple para gestionar tareas TODO construida con FastAPI y Supabase.

## Características

- ✅ Crear tareas
- ✅ Listar todas las tareas
- ✅ Obtener tarea por ID
- ✅ Actualizar tareas
- ✅ Eliminar tareas
- ✅ Filtrar por estado y prioridad
- ✅ Documentación automática con Swagger

## Instalación

1. Clonar el repositorio
2. Instalar dependencias:
   ```bash
   uv install
   ```

3. Configurar variables de entorno:
   - Copiar `.env.example` a `.env`
   - Completar con tus credenciales de Supabase

4. Crear la tabla en Supabase usando el archivo `todo.sql`

## Ejecución

```bash
python main.py
```

La API estará disponible en: http://localhost:8000

## Documentación

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Endpoints

### Tareas

- `GET /` - Mensaje de bienvenida
- `GET /health` - Estado de la API
- `POST /tasks/` - Crear nueva tarea
- `GET /tasks/` - Listar todas las tareas (con filtros opcionales)
- `GET /tasks/{task_id}` - Obtener tarea por ID
- `PUT /tasks/{task_id}` - Actualizar tarea
- `DELETE /tasks/{task_id}` - Eliminar tarea
- `GET /tasks/status/{status}` - Obtener tareas por estado

### Ejemplos de uso

#### Crear una tarea
```bash
curl -X POST "http://localhost:8000/tasks/" \
-H "Content-Type: application/json" \
-d '{
  "title": "Mi primera tarea",
  "description": "Descripción de la tarea",
  "status": "To Do",
  "priority": 1
}'
```

#### Obtener todas las tareas
```bash
curl -X GET "http://localhost:8000/tasks/"
```

#### Filtrar tareas por estado
```bash
curl -X GET "http://localhost:8000/tasks/?status_filter=To Do"
```

#### Actualizar una tarea
```bash
curl -X PUT "http://localhost:8000/tasks/1" \
-H "Content-Type: application/json" \
-d '{
  "status": "Done"
}'
```

## Estados disponibles

- `To Do` - Por hacer
- `In Progress` - En progreso
- `Done` - Completado

## Estructura del proyecto

```
.
├── main.py          # Aplicación principal de FastAPI
├── pyproject.toml   # Configuración del proyecto y dependencias
├── todo.sql         # Script para crear la tabla en la base de datos
├── .env.example     # Ejemplo de variables de entorno
└── README.md        # Este archivo
```

## Tecnologías utilizadas

- **FastAPI** - Framework web moderno y rápido
- **Supabase** - Base de datos PostgreSQL como servicio
- **Pydantic** - Validación de datos
- **Uvicorn** - Servidor ASGI
- **python-dotenv** - Manejo de variables de entorno
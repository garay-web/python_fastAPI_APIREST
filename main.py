# API REST: Interfaz de Programación de Aplicaciones para compartir recursos
from typing import List, Optional
import uuid
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel


# Inicializamos una variable donde tendrá todas las características de una API REST
app = FastAPI()


# Acá definimos el modelo ________________*

class Curso(BaseModel):
    id: Optional[str] = None
    nombre: str
    descripcion: Optional[str] = None
    nivel: str
    duracion: int
#                         _________________|


# Simularemos una base de datos
cursos_db = []


# CRUD: Read (lectura) --> *_GET ALL_*: Leeremos todos los cursos que haya en la db ____________(Lectura de todos los cursos 'GET ALL')
@app.get("/cursos/", response_model=List[Curso])
def obtener_cursos():
    return cursos_db

# CRUD: Create (escribir) --> *_POST_*: agregaremos un nuevo curso a nuestra base de datos ___(Escritura)
@app.post("/cursos/", response_model=Curso)
def crear_curso(curso:Curso):
    curso.id = str(uuid.uuid4()) # _______> Usamos UUID para generar un ID único e irrepetible<______
    cursos_db.append(curso)
    return curso

# CRUD: Read (lectura) --> *_GET_*: (individual): Leeremos el curso que coincida con el ID que pidamos _______(Lectura de un curso con ID único)
@app.get("/cursos/{curso_id}", response_model=Curso)
def obtener_curso(curso_id:str):
    curso = next((curso for curso in cursos_db if curso.id == curso_id), None) # Con next tomamos la primera coincidencia del array devuelto
    if curso is None:
        raise HTTPException(status_code=404, detail="Curso no encontrado")
    return curso

# CRUD: Update (Actualizar/Modificar) --> *_PUT_*: Modificaremos un recurso que coincida con el ID que mandemos
@app.put("/cursos/{curso_id}", response_model=Curso)
def actualizar_curso(curso_id:str, curso_actualizado:Curso):
    curso = next((curso for curso in cursos_db if curso.id == curso_id), None) # Con next tomamos la primera coincidencia del array devuelto
    if curso is None:
        raise HTTPException(status_code=404, detail="Curso no encontrado")
    curso_actualizado.id = curso_id
    index = cursos_db.index(curso) # Buscamos el índice exacto donde está el curso en nuestra lista (DB)
    cursos_db[index] = curso_actualizado
    return curso_actualizado

# CRUD: Delete (borrado/baja) --> *_DELETE_*: 'Eliminaremos un recurso que coincida con el ID que mandemos'
@app.delete("/cursos/{curso_id}", response_model=Curso)
def eliminar_curso(curso_id:str):
    curso = next((curso for curso in cursos_db if curso.id == curso_id), None) # Con next tomamos la primera coincidencia del array devuelto
    if curso is None:
        raise HTTPException(status_code=404, detail="Curso no encontrado")
    cursos_db.remove(curso)
    return curso
from fastapi import FastAPI, BackgroundTasks, HTTPException, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
import app.crud as crud
from sqlalchemy.orm import Session
from fastapi.templating import Jinja2Templates
from . import schemas
from app.database import get_db
from . import models
from app.database import engine
from app.utils import perform_translation

# imports in another way
import app.crud as crud
import app.schemas as schemas
from app.database import get_db, engine

# create the models, makes sure database exists when FastAPI load up
models.Base.metadata.create_all(bind=engine)
app = FastAPI()

# Enable CORS: Cross Origin Resource Sharing
# controls how resources on a web server can be requested from another domain. like website interacting with API host site
# safe/secure data sharing between different domains
# CORSMiddleware: adds necessary HTTP headers to responses to allow browsers to make cross-origin requests.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Allows all origins
    allow_credentials=True, # Allows cookies to be included in corss-origin requests
    allow_methods=["*"], # Allows all methods for cross-origin requests
    allow_headers=["*"], # Allows all headers in the resquests
)

# setup for jinja2 templates
templates = Jinja2Templates(directory="app/templates")

# webpage setup --> setup localhost:8000/index in url
@app.get('/index', response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# endpoints for handeling data: GET, POST, PUT, DELETE <-- HTTP Methods

@app.post("/translate", response_model=schemas.TaskResponse)
# Front-end sends post request to the /translate endpoint.
# server creates a translation task and returns a 'task_id'
# front-end stores this task_id and could periodically check the task status
def translate(request: schemas.TranslationRequest, background_tasks: BackgroundTasks, db: Session= Depends(get_db)):
    # create a new translation task when user submits a translation request.
    # Follows TranslationRequest format

    task = crud.create_translation_task(db, request.text, request.languages)
    background_tasks.add_task(perform_translation, task.id, request.text, request.languages, db)
    return {"task_id": {task.id}}


@app.get("/translate/{task_id}", response_model=schemas.TranslationStatus)
# Front-end sends GET request to /translate/id with the specific task_id
# server returns status and possibly translation of the task.
# front-end updates UI based from that response.
def get_translate(task_id: int, db: Session = Depends(get_db)):
    # FOR CHECK STATUS BUTTON
    task = crud.get_translation_task(db, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="task not found")
    return{"task_id": task.id, "status":task.status, "translation":task.translations}



@app.get("/translate/content/{task_id}", response_model=schemas.TranslationStatus)
# Frontend sents a GET request to /translate/content/id with the specific task_id.
# Server returns full content of the translation task
# Frontend displays translation content
def get_translate_content(task_id: int, db: Session = Depends(get_db)):
    # FOR CHECK CONTENT BUTTON
    task = crud.get_translation_task(db, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="task not found")
    return {task} # return full task object


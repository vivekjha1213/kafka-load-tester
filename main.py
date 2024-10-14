from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os
from producer import start_producing
from consumer import start_consuming

app = FastAPI()


app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/create-dir/")
async def create_directory(dir_name: str = Form(...)):
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)
        message = f"Directory '{dir_name}' created."
    else:
        message = f"Directory '{dir_name}' already exists."
    return templates.TemplateResponse("index.html", {"request": {}, "message": message})

# Create or update a file (touch equivalent)
@app.post("/touch-file/")
async def touch_file(file_name: str = Form(...)):
    with open(file_name, 'a'):
        os.utime(file_name, None)
    message = f"File '{file_name}' created or updated."
    return templates.TemplateResponse("index.html", {"request": {}, "message": message})

# Start producing Kafka messages
@app.post("/start-producer/")
async def start_producer(topic: str = Form(...), num_messages: int = Form(...)):
    start_producing(topic, num_messages)
    message = f"Started producing {num_messages} messages to topic '{topic}'."
    return templates.TemplateResponse("index.html", {"request": {}, "message": message})

# Start consuming Kafka messages
@app.post("/start-consumer/")
async def start_consumer(topic: str = Form(...)):
    start_consuming(topic)
    message = f"Started consuming messages from topic '{topic}'."
    return templates.TemplateResponse("index.html", {"request": {}, "message": message})

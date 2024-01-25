from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
import pandas as pd
from pydantic import BaseModel



app = FastAPI()



tasks = []

class Task(BaseModel):
    id: int
    title: str
    description: str
    status: str


@app.get("/tasks", response_class=HTMLResponse)
async def get_task(request: Request):
    task_table = pd.DataFrame([vars(task)for task in tasks]).to_html()
    return task_table

@app.get("/tasks/look/{task_id}")
async def look_task(task_id: int, task: Task):
    for i, store_task in enumerate(tasks):
        if store_task.id == task_id:
            return task



@app.post("/tasks", response_model=Task)
async def add_task(task: Task):
    tasks.append(task)
    return task

@app.put("/tasks/{task_id}", response_model=Task)
async def update_task(task_id: int, task: Task):
    for i, store_task in enumerate(tasks):
        if store_task.id == task_id:
            task.id = task_id
            task[i] = task
            return task

@app.delete("/tasks/del/{task_id}", response_class=HTMLResponse)
async def delete_task(request: Request, task_id: int):
    for i, store_task in enumerate(tasks):
        if store_task.id == task_id:
            return pd.DataFrame([vars(tasks.pop(i))]).to_html()

from time import sleep
from fastapi import FastAPI, WebSocket, BackgroundTasks

from fastapi.middleware.cors import CORSMiddleware
from utils.promptconfig import PromptConfig
from utils.template_engine import TemplateEngine
from utils.experiments import Experiments
from utils.analyser import ConfigurationAnalyser
from utils.results import Results
from utils.db_connector import DBConnector
from uuid import uuid4

app = FastAPI()
origins = [
    "http://localhost",
    "http://localhost:3000",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

tasks = {}

db_instance = DBConnector()


@app.get("/")
async def root():
    return {"message": "Hello, World!"}


@app.post("/experiment/init")
async def init_experiment(data: dict, background_tasks: BackgroundTasks):
    # Validate the data
    analyser = ConfigurationAnalyser(data)
    validation_message, validation_result = analyser.validate_data()
    if not validation_result:
        return {"error": validation_message}
    # genereate a unique id for the project
    project_id = str(uuid4())

    # initdb and initexperiment
    exp = Experiments(project_id, data)
    background_tasks.add_task(exp.init)
    return {"message": "Experiment initialized!", "exp_id": project_id}


@app.websocket("/experiment/status/{exp_id}")
async def experiment_status(websocket: WebSocket, exp_id: str):
    websocket.accept()
    if exp_id not in tasks:
        websocket.send_json({"error": "Experiment not found"})
        return
    task = tasks[exp_id]
    while task.is_alive():
        websocket.send_json({"status": "running"})
        sleep(1)
    task.join()
    websocket.send_json({"status": "completed"})


@app.get("/experiment/results/{exp_id}")
async def experiment_results(exp_id: str):
    if not db_instance.is_project_exists(exp_id):
        return {"error": "Experiment not found"}
    r = Results(exp_id)
    return r.get_results()


@app.get("/experiment/listall")
async def experiment_listall():
    return db_instance.get_projects()


@app.get("/test/promptTemplate/{exp_id}")
async def test_prompt_template(exp_id: str):
    app.state.prompt = PromptConfig(app.state.config, app.state.dataset)
    return {"prompt": app.state.prompt}


@app.get("/test/promptTokens/{exp_id}")
async def test_prompt_tokens(exp_id: str):
    print(app.state.tokens)
    return {"tokens": app.state.tokens}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)

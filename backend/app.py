from time import sleep
from fastapi import FastAPI, WebSocket, BackgroundTasks
from utils.promptconfig import PromptConfig
from utils.template_engine import TemplateEngine
from utils.experiments import Experiments
from utils.analyser import ConfigurationAnalyser
from uuid import uuid4

app = FastAPI()

tasks = {}


@app.get("/")
async def root():
    return {"message": "Hello, World!"}


@app.post("/experiment/init")
async def init_experiment(data: dict, background_tasks: BackgroundTasks):
    # Validate the data
    analyser = ConfigurationAnalyser(data)
    validation_result = analyser.validate_data()

    # genereate a unique id for the project
    project_id = str(uuid4())

    # initdb and initexperiment
    exp = Experiments(project_id, data)
    background_tasks.add_task(exp.init)
    if not validation_result:
        return {"error": validation_result}
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


@app.get("/test/promptTemplate/{exp_id}")
async def test_prompt_template(exp_id: str):
    print(app.state.prompt)
    return {"prompt": app.state.prompt}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)

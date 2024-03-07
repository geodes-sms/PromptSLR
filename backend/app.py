import asyncio
from fastapi import FastAPI, WebSocket
from utils.experiments import Experiments
from utils.analyser import ConfigurationAnalyser

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello, World!"}


@app.post("/experiment/init")
async def init_experiment(data: dict):
    # Validate the data
    analyser = ConfigurationAnalyser(data)
    validation_result = analyser.validate_data()

    if validation_result is not True:
        return {"error": validation_result}
    return {"message": "Experiment initialized!"}


@app.websocket("/experiment/status")
async def experiment_status(websocket: WebSocket):
    await websocket.accept()

    while True:
        # Check the status of the process here
        status = Experiments.check_process_status()

        # Send the status to the client
        await websocket.send_json({"status": status})

        # Wait for a while before checking the status again
        await asyncio.sleep(5)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)

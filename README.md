# PromptSLR
Instructions to run
## Backend
Run the following scripts in the `backend` directory:

1. Create a conda environment using the following command:
```bash
conda create env -f env.yml
```

### Setup Prisma
1. Install MySQL or PostgreSQL(currently used in the project) and create a database.
2. Modfiy the connection string on line 3 in `backend/utils/schema/schema.prisma` to point to your database.
3. Run the following commands in the `backend` directory:
```bash
prisma db push --schema utils/schema/schema.prisma
```

### Run the server
1. Run the following command in the `backend` directory:
```bash
python app.py
```
> It will start the server on [http://localhost:8000](http://localhost:8000)

## Testing
You can follow the UI to test the Application.

Also, you can use the following API endpoints to test the application:
1. goto [http://localhost:8000/docs](http://localhost:8000/docs) to test the API endpoints.
2. Try the `/experiment/init` endpoint to initialize the experiment from the Swagger UI.
    Sample configuration to try for random Classifier.
    ```json
    {
        "project": {
            "name": "Random RL4SE",
            "topic": {
                "title": "RL4SE"
            }
        },
        "llm": {
            "name": "random",
            "hyperparams": {
                "isTrainable": false,
                "additional": {
                    "seed": 123
                }
            }
        },
        "dataset": {
            "name": "rl4se"
        },
        "configurations": {
            "features": [
                "title",
                "abstract"
            ],
            "linient": true,
            "shots": {
                "positive": 3,
                "negative": 1
            },
            "selectionCriteria": {
                "inclusion": {
                    "condition": [
                        "any"
                    ],
                    "criteria": [
                        "Title containing Reinforcement."
                    ]
                },
                "exclusion": {
                    "condition": [
                        "any"
                    ],
                    "criteria": [
                        "Papers published before 2006"
                    ]
                }
            },
            "output": {
                "classes": 2
            }
        }
    }
    ```
3. To get all the results of the experiment, try the `/experiment/results` endpoint. You need to provide the `exp_id` parameter which is the experiment id you get from the `/experiment/init` endpoint in the response.

> Note: A sample dataset is already present in the `backend/data` directory. You can use it to test the application.

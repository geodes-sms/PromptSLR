from backend.utils.datasets import Datasets
from backend.utils.db_connector import DBConnector
from backend.utils.scheduler import Scheduler


class Experiments:

    def __init__(self, project_id: str, config: dict):
        self.project_id = project_id
        self.config = config
        self.db_connector = DBConnector()

    def init(self):
        if not self.is_experiment_exists():
            self.init_db()
            self.init_experiment()

    def is_experiment_exists(self):
        return self.db_connector.is_project_exists(self.project_id)

    def init_db(self):
        self.db_connector.create_project(
            self.project_id,
            self.config["project"]["name"],
            self.config["project"]["topic"]["title"],
            self.config["project"]["topic"]["description"],
        )
        self.db_connector.create_llm(
            self.project_id,
            self.config["llm"]["name"],
            self.config["llm"]["url"],
            self.config["llm"]["apikey"],
            self.config["llm"]["hyperparams"]["default"]["temperature"],
            self.config["llm"]["hyperparams"]["default"]["maxTokens"],
        )
        for key, value in self.config["llm"]["hyperparams"]["additional"].items():
            self.db_connector.create_llmhyparams(
                self.db_connector.get_llmid(self.project_id),
                key,
                value,
            )
        if not self.db_connector.is_dataset_exists(self.config["dataset"]["name"]):
            datatsets = Datasets()
            datatsets.load_data()

        self.db_connector.create_project_dataset(
            self.project_id,
            self.db_connector.get_datasetid(self.config["dataset"]["name"]),
        )

        self.db_connector.create_configurations(self.project_id, self.config)

    def init_experiment(self):
        self.scheduler = Scheduler(self.config)
        self.scheduler.schedule()

    @staticmethod
    def check_process_status(self, project_id: str):
        return self.db_connector.get_project_status(project_id)

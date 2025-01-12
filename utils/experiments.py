from utils.datasets import Datasets
from utils.db_connector import DBConnector
from utils.promptconfig import PromptConfig
from utils.scheduler import Scheduler
from utils.template_engine import TemplateEngine


class Experiments:

    def __init__(self, project_id: str, config: dict, progress_bar=None, template_name: str = "lc/lc_simple.jinja"):
        self.template_name = template_name
        self.project_id = project_id
        self.config = config
        self.db_connector = DBConnector()
        self.progress_bar = progress_bar or None

    def init(self):
        if not self.is_experiment_exists():
            self.init_db()
            self.init_experiment()
            return True
        else:
            return False

    def is_experiment_exists(self):
        return self.db_connector.is_project_exists(self.project_id)

    def init_db(self):
        self.db_connector.create_project(
            self.project_id,
            self.config["project"]["name"],
            self.config["project"]["topic"]["title"],
            (
                self.config["project"]["topic"]["description"]
                if "description" in self.config["project"]["topic"]
                else None
            ),
            iterations=self.config["project"]["iterations"],
        )
        self.db_connector.create_llm(
            self.project_id,
            self.config["llm"]["name"],
            self.config["llm"]["url"] if "url" in self.config["llm"] else None,
            self.config["llm"]["apikey"] if "apikey" in self.config["llm"] else None,
            (
                self.config["llm"]["hyperparams"]["default"]["temperature"]
                if "default" in self.config["llm"]["hyperparams"]
                else None
            ),
            (
                self.config["llm"]["hyperparams"]["default"]["maxTokens"]
                if "default" in self.config["llm"]["hyperparams"]
                else None
            ),
        )
        if "additional" in self.config["llm"]["hyperparams"]:
            for key, value in self.config["llm"]["hyperparams"]["additional"].items():
                self.db_connector.create_llmhyparams(
                    self.db_connector.get_llmid(self.project_id),
                    key,
                    str(value),
                )
        self.datasets = Datasets(config=self.config, project_id=self.project_id)
        if not self.db_connector.is_dataset_exists(self.config["dataset"]["name"]):
            self.datasets.create_dataset()
            self.datasets.load_data()

        self.db_connector.create_project_dataset(
            self.project_id,
            self.db_connector.get_datasetid(self.config["dataset"]["name"]),
        )
        prompt_config = PromptConfig(self.config, self.datasets)
        self.templateEngine = TemplateEngine()
        self.context = self.templateEngine.render(promptConfig=prompt_config,template_name=self.template_name)
        self.db_connector.create_configurations(
            self.project_id,
            self.config,
            renderdPrompt=self.context,
        )

    def init_experiment(self):
        self.scheduler = Scheduler(
            self.config,
            self.project_id,
            self.datasets,
            self.progress_bar,
            self.context,
            self.templateEngine.get_tokens(),
        )
        self.scheduler.schedule()

    @staticmethod
    def check_process_status(self, project_id: str):
        return self.db_connector.get_project_status(project_id)

import time
from backend.utils.datasets import Datasets
from backend.utils.db_connector import DBConnector
from backend.utils.model import (
    ChatGPT,
    ComplementNaiveBayes,
    LlamaFile,
    LogisticRegression,
    MultiNaiveBayes,
    Random,
    RandomForest,
    SupportVectorMachine,
)
from backend.utils.output import CorrectAnswer, Output
from backend.utils.promptconfig import PromptConfig
from backend.utils.template_engine import TemplateEngine
import concurrent.futures


class Scheduler:
    def __init__(self, config: dict, project_id: str):
        self.config = config
        self.model = self.get_model()
        self.db_connector = DBConnector()
        self.dataset = Datasets(config=config, project_id=project_id)
        self.dataset.load_data()
        prompt_config = PromptConfig(config)
        templateEngine = TemplateEngine()
        self.context = templateEngine.render(promptConfig=prompt_config)
        self.rate_limit = 50

    def get_model(self):
        if self.config["llm"]["name"] == "chatgpt":
            return ChatGPT(self.config)
        elif self.config["llm"]["name"] == "llamafile":
            return LlamaFile(self.config)
        elif self.config["llm"]["name"] == "lr":
            return LogisticRegression(self.config)
        elif self.config["llm"]["name"] == "svm":
            return SupportVectorMachine(self.config)
        elif self.config["llm"]["name"] == "mnb":
            return MultiNaiveBayes(self.config)
        elif self.config["llm"]["name"] == "cnb":
            return ComplementNaiveBayes(self.config)
        elif self.config["llm"]["name"] == "rf":
            return RandomForest(self.config)
        elif self.config["llm"]["name"] == "random":
            return Random(self.config)
        else:
            raise ValueError(f"Model {self.config['llm']['name']} not supported")

    def schedule(self):
        requests = 0
        responses = []
        with concurrent.futures.ThreadPoolExecutor(
            max_workers=self.rate_limit
        ) as executor:
            for article in self.dataset.get_articles():
                requests += 1
                try:
                    answer = executor.submit(self.model.api_decide, article)
                    responses.append(answer)
                    self.output = Output(answer.choices[0].message.content)
                    self.correctOutput = CorrectAnswer(article["ScreenedDecision"])
                    self.db_connector.create_llmdecision(
                        artileKey=article["Key"],
                        decision=self.output.get_decision(),
                        projectID=self.project_id,
                        error=False,
                        retries=0,
                        rawOutput=answer.choices[0].message.content,
                        reason=self.output.reason,
                        confidence=self.output.confidence,
                    )
                except Exception as e:
                    self.db_connector.create_llmdecision(
                        artileKey=article["Key"],
                        decision=e.__str__(),
                        projectID=self.project_id,
                        error=True,
                        retries=1,
                    )
                if requests >= self.rate_limit and isinstance(self.model, ChatGPT):
                    print("Waiting for the rate limit to reset......")
                    time.sleep(60)
                    requests = 0

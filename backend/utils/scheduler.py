import time
from utils.datasets import Datasets
from utils.db_connector import DBConnector
from utils.model import (
    ChatGPT,
    ComplementNaiveBayes,
    LlamaFile,
    LogisticRegression,
    MultiNaiveBayes,
    Random,
    RandomForest,
    SupportVectorMachine,
)
from utils.output import CorrectAnswer, Output
from utils.promptconfig import PromptConfig
from utils.template_engine import TemplateEngine
import concurrent.futures


class Scheduler:
    def __init__(self, config: dict, project_id: str, dataset: Datasets = None):
        self.config = config
        self.project_id = project_id
        self.dataset = dataset
        self.db_connector = DBConnector()
        prompt_config = PromptConfig(config, self.dataset)
        templateEngine = TemplateEngine()
        self.context = templateEngine.render(promptConfig=prompt_config)
        self.rate_limit = 50
        self.model = self.get_model()

    def get_model(self):
        if "gpt" in self.config["llm"]["name"]:
            return ChatGPT(context=self.context, parameters=self.config)
        elif self.config["llm"]["name"] == "llamafile":
            return LlamaFile(context=self.context, parameters=self.config)
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
            return Random(context=self.context, parameters=self.config)
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
                answer = executor.submit(
                    self.model.api_decide, self.format_article(article), article
                )
                responses.append(answer)
                if requests >= self.rate_limit and isinstance(self.model, ChatGPT):
                    print("Waiting for the rate limit to reset......")
                    time.sleep(60)
                    requests = 0
        for response in concurrent.futures.as_completed(responses):
            answer, article = response.result()
            try:
                self.db_connector.create_llmdecision(
                    artileKey=article.Key,
                    decision=answer.decision,
                    projectID=self.project_id,
                    error=False,
                    retries=0,
                    rawOutput=answer.content,
                    reason=answer.reason,
                    confidence=answer.confidence,
                )
            except Exception as e:
                self.db_connector.create_llmdecision(
                    artileKey=article.Key,
                    decision=e.__str__(),
                    projectID=self.project_id,
                    error=True,
                    retries=1,
                )

    def format_article(self, article):
        tmp = {}
        for i in self.config["configurations"]["features"]:
            tmp[i] = getattr(article, i.title())
        fmt_article = []
        for k, v in tmp.items():
            fmt_article.append(f"- {k.title()}: {v.strip()}")
        return "\n".join(fmt_article)

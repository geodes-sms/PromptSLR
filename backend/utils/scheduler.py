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
        print(len(self.dataset.get_articles()))
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
        llm_decisions = []
        for response in concurrent.futures.as_completed(responses):
            answer, article = response.result()
            try:
                llm_decisions.append(
                    {
                        "LLMID": self.db_connector.get_llmid(self.project_id),
                        "ArticleKey": article.Key,
                        "ProjectID": self.project_id,
                        "Decision": answer.decision,
                        "Error": False,
                        "Retries": 0,
                        "RawOutput": answer.content,
                        "Reason": answer.reason,
                        "Confidence": answer.confidence,
                    }
                )
            except Exception as e:
                llm_decisions.append(
                    {
                        "LLMID": self.db_connector.get_llmid(self.project_id),
                        "ArticleKey": article.Key,
                        "ProjectID": self.project_id,
                        "Decision": e.__str__(),
                        "Error": True,
                        "Retries": 1,
                    }
                )
        self.db_connector.db.llmdecisions.create_many(llm_decisions)

    def format_article(self, article):
        tmp = {}
        for i in self.config["configurations"]["features"]:
            tmp[i] = getattr(article, i.title())
        fmt_article = []
        for k, v in tmp.items():
            fmt_article.append(f"- {k.title()}: {v.strip()}")
        return "\n".join(fmt_article)
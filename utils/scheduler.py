import os
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
import csv
import concurrent.futures


class Scheduler:
    def __init__(
        self, config: dict, project_id: str, dataset: Datasets = None, progress_bar=None
    ):
        self.config = config
        self.project_id = project_id
        self.dataset = dataset
        self.progress_bar = progress_bar
        self.db_connector = DBConnector()
        prompt_config = PromptConfig(config, self.dataset)
        templateEngine = TemplateEngine()
        self.context = templateEngine.render(promptConfig=prompt_config)
        self.db_connector.db.projects.update(
            where={
                "ProjectID": self.project_id,
            },
            data={
                "ContextTokens": templateEngine.get_tokens(),
            },
        )
        self.rate_limit = 50
        self.max_retries = 5
        self.iterations = int(self.config["project"]["iterations"])
        self.vectorizer_parameters = {"min_count": 3, "workers": 4}
        self.trainable_parameters = {
            "seed": (
                self.config["llm"]["hyperparams"]["additional"]["seed"]
                if "seed" in self.config["llm"]["hyperparams"]["additional"]
                else None
            ),
            "fold_count": (
                self.config["llm"]["hyperparams"]["additional"]["fold_count"]
                if "fold_count" in self.config["llm"]["hyperparams"]["additional"]
                else None
            ),
            "epoch": (
                self.config["llm"]["hyperparams"]["additional"]["epoch"]
                if "epoch" in self.config["llm"]["hyperparams"]["additional"]
                else None
            ),
        }
        self.model = self.get_model()

    def get_model(self):
        if "gpt" in self.config["llm"]["name"]:
            return ChatGPT(context=self.context, parameters=self.config)
        elif self.config["llm"]["name"] == "llamafile":
            return LlamaFile(context=self.context, parameters=self.config)
        elif self.config["llm"]["name"] == "lr":
            return LogisticRegression(
                context=self.context, vectorizer_parameters=self.vectorizer_parameters
            )
        elif self.config["llm"]["name"] == "svm":
            return SupportVectorMachine(
                context=self.context, vectorizer_parameters=self.vectorizer_parameters
            )
        elif self.config["llm"]["name"] == "mnb":
            return MultiNaiveBayes(
                context=self.context, vectorizer_parameters=self.vectorizer_parameters
            )
        elif self.config["llm"]["name"] == "cnb":
            return ComplementNaiveBayes(
                context=self.context, vectorizer_parameters=self.vectorizer_parameters
            )
        elif self.config["llm"]["name"] == "rf":
            return RandomForest(
                context=self.context, vectorizer_parameters=self.vectorizer_parameters
            )
        elif self.config["llm"]["name"] == "random":
            return Random(context=self.context, parameters=self.config)
        else:
            raise ValueError(f"Model {self.config['llm']['name']} not supported")

    def schedule(self):
        for iter in range(self.iterations):
            if self.config["llm"]["hyperparams"]["isTrainable"]:
                self.run_trainable(iter)
            else:
                retries = 0
                # while (
                #     not (self.db_connector.is_error_present(self.project_id))
                #     and retries < self.max_retries
                # ):
                while retries < self.max_retries:
                    # TODO: Add a retry mechanism and fix loop for error handling
                    print("Retries: ", retries)
                    if (
                        not self.db_connector.is_error_present(self.project_id)
                        and retries > 0
                    ):
                        break
                    elif retries == 0:
                        self.run(iter=iter)
                    else:
                        self.run(iter=iter, retries=retries)
                    retries += 1

    def run(self, iter, retries=None):
        requests = 0
        counts = 0
        responses = []
        articles = self.dataset.get_articles(retries=retries)
        print(len(articles))
        with concurrent.futures.ThreadPoolExecutor(
            max_workers=self.rate_limit
        ) as executor:
            for article in articles:
                requests += 1
                counts += 1
                answer = executor.submit(
                    self.model.api_decide, self.format_article(article), article
                )
                responses.append(answer)
                self.progress_bar.progress(counts / len(articles))
                self.progress_bar.text(f"Progress: {counts}/{len(articles)}")
                if requests >= self.rate_limit and isinstance(self.model, ChatGPT):
                    print("Waiting for the rate limit to reset......")
                    time.sleep(60)
                    requests = 0
        llm_decisions = []
        llm_errors = []
        for response in concurrent.futures.as_completed(responses):
            try:
                answer, article = response.result()
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
                        "Confidence": (
                            float(answer.confidence) if answer.confidence else None
                        ),
                        "TokenUsed": (
                            int(answer.token_used) if answer.token_used else None
                        ),
                        "Iteration": iter,
                    }
                )
            except Exception as e:
                llm_errors.append(
                    {
                        "LLMID": self.db_connector.get_llmid(self.project_id),
                        "ArticleKey": article.Key,
                        "ProjectID": self.project_id,
                        "Decision": e.__str__(),
                        "Error": True,
                        "Retries": 0 if not retries else retries,
                        "RawOutput": None,
                        "Reason": None,
                        "Confidence": None,
                        "TokenUsed": None,
                        "Iteration": iter,
                    }
                )
        if not retries or retries == 0:
            self.db_connector.db.llmdecisions.create_many(llm_decisions)
            self.db_connector.db.llmdecisions.create_many(llm_errors)
        else:
            self.db_connector.db.llmdecisions.update_many(llm_decisions, {})
            self.db_connector.db.llmdecisions.update_many(llm_errors, {})

    def run_trainable(self, iter):
        articles = self.dataset.get_articles()
        print(len(articles))
        llm_decisions = []
        llm_errors = []
        path_prefix = "models"
        self.model_path = os.path.join(path_prefix, "f{self.project_id}.bin")
        self.model_vectorizer_path = os.path.join(
            path_prefix, "f{self.project_id}_word2vec.bin"
        )
        if os.path.exists(self.model_path) and os.path.exists(
            self.model_vectorizer_path
        ):
            self.model.load()
        else:
            if not os.path.exists(path_prefix):
                os.makedirs(path_prefix)
            self.model.train(
                data=articles,
                training_parameters=self.trainable_parameters,
            )
            self.model.save(path=path_prefix, filename=self.project_id)

        for count, article in enumerate(articles):
            try:
                answer, article = self.model.api_decide(article=article)
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
                        "Confidence": (
                            float(answer.confidence) if answer.confidence else None
                        ),
                        "TokenUsed": (
                            int(answer.token_used) if answer.token_used else None
                        ),
                        "Iteration": iter,
                    }
                )
            except Exception as e:
                llm_errors.append(
                    {
                        "LLMID": self.db_connector.get_llmid(self.project_id),
                        "ArticleKey": article.Key,
                        "ProjectID": self.project_id,
                        "Decision": e.__str__(),
                        "Error": True,
                        "Retries": 0,
                        "RawOutput": None,
                        "Reason": None,
                        "Confidence": None,
                        "TokenUsed": None,
                        "Iteration": iter,
                    }
                )
            self.progress_bar.progress(count / len(articles))
            self.progress_bar.text(f"Progress: {count}/{len(articles)}")
        self.db_connector.db.llmdecisions.create_many(llm_decisions)
        self.db_connector.db.llmdecisions.create_many(llm_errors)
        print("Created LLM Decisions")

    def format_article(self, article):
        tmp = {}
        for i in self.config["configurations"]["features"]:
            tmp[i] = getattr(article, i.title())
        fmt_article = []
        for k, v in tmp.items():
            fmt_article.append(f"- {k.title()}: {v.strip()}")
        return "\n".join(fmt_article)

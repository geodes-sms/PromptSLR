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
import concurrent.futures


class Scheduler:
    def __init__(
        self,
        config: dict,
        project_id: str,
        dataset: Datasets = None,
        progress_bar=None,
        context: str = None,
        context_tokens: int = None,
    ):
        self.config = config
        self.project_id = project_id
        self.dataset = dataset
        self.progress_bar = progress_bar or None
        self.db_connector = DBConnector()
        self.context = context
        self.db_connector.db.projects.update(
            where={
                "ProjectID": self.project_id,
            },
            data={
                "ContextTokens": context_tokens,
            },
        )
        self.rate_limit = 120
        self.max_retries = 25
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
                while retries < self.max_retries:

                    print("Retries: ", retries)
                    is_error_present = self.db_connector.is_error_present(
                        self.project_id
                    )
                    print("Error Present: ", is_error_present)
                    if (not is_error_present) and retries > 0:
                        break
                    elif retries == 0:
                        self.run(iter=iter)
                    else:
                        time.sleep(60)
                        print("Retrying......")
                        self.run(iter=iter, retries=retries)
                    retries += 1

    def run(self, iter, retries=None):
        requests = 0
        counts = 0
        responses = []
        articles, error_decisions = self.dataset.get_articles(retries=retries)
        print(len(articles))

        # Map article keys to existing decisions for quick lookup
        decision_map = (
            {err.ArticleKey: err for err in error_decisions} if error_decisions else {}
        )

        with concurrent.futures.ThreadPoolExecutor(
            max_workers=self.rate_limit
        ) as executor:
            for article in articles:
                requests += 1
                counts += 1
                response = executor.submit(
                    self.model.api_decide, self.format_article(article), article
                )
                responses.append((response, article))
                if self.progress_bar:
                    self.progress_bar.progress(counts / len(articles))
                    self.progress_bar.text(f"Progress: {counts}/{len(articles)}")
                if requests >= self.rate_limit and isinstance(self.model, ChatGPT):
                    print("Waiting for the rate limit to reset......")
                    time.sleep(60)
                    requests = 0

        llm_decisions = []
        llm_errors = []

        for future, article in responses:
            try:
                answer, _ = future.result()
                decision_data = {
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
                    "TokenUsed": int(answer.token_used) if answer.token_used else None,
                    "Iteration": iter,
                }

                existing_decision = decision_map.get(article.Key)
                if existing_decision:
                    decision_data["DecisionID"] = existing_decision.DecisionID
                    decision_data["Retries"] = existing_decision.Retries + 1
                llm_decisions.append(decision_data)

            except Exception as e:
                error_data = {
                    "LLMID": self.db_connector.get_llmid(self.project_id),
                    "ArticleKey": article.Key,
                    "ProjectID": self.project_id,
                    "Decision": str(e),
                    "Error": True,
                    "Retries": retries + 1 if retries else 1,
                    "RawOutput": None,
                    "Reason": None,
                    "Confidence": None,
                    "TokenUsed": None,
                    "Iteration": iter,
                }

                existing_decision = decision_map.get(article.Key)
                if existing_decision:
                    error_data["DecisionID"] = existing_decision.DecisionID
                    error_data["Retries"] = existing_decision.Retries + 1
                llm_errors.append(error_data)

        if not retries or retries == 0:
            self.db_connector.db.llmdecisions.create_many(llm_decisions)
            self.db_connector.db.llmdecisions.create_many(llm_errors)
        else:
            for decision in llm_decisions:
                if "DecisionID" in decision:
                    self.db_connector.db.llmdecisions.update_many(
                        where={"DecisionID": decision["DecisionID"]}, data=decision
                    )
                else:
                    self.db_connector.db.llmdecisions.create(decision)
            for error in llm_errors:
                if "DecisionID" in error:
                    self.db_connector.db.llmdecisions.update_many(
                        where={"DecisionID": error["DecisionID"]}, data=error
                    )
                else:
                    self.db_connector.db.llmdecisions.create(error)

    def run_trainable(self, iter):
        articles, _ = self.dataset.get_articles()
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
            if self.progress_bar:
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

import os
import pandas as pd
import random
from utils.db_connector import DBConnector


class Datasets:
    def __init__(
        self, data_dir: str = None, config: dict = None, project_id: str = None
    ):
        self.config = config
        if not data_dir:
            self.data_dir = os.path.join(os.getcwd(), "data")
        else:
            self.data_dir = data_dir
        self.project_id = project_id
        self.db_connector = DBConnector()

    def create_dataset(self):
        self.dataset = self.db_connector.create_dataset(
            name=self.config["dataset"]["name"], projectID=self.project_id
        )

    def load_data(self):
        self.df = pd.read_csv(
            os.path.join(
                self.data_dir, f"{self.config['dataset']['name'].lower()}.csv"
            ),
            sep="\t",
            na_values=[None],
            keep_default_na=False,
        )
        print(self.df.shape)
        articles = []
        for i in self.df.itertuples():
            articles.append(
                self.db_connector.create_article_dict(
                    key=str(i.key),
                    abstract=str(i.abstract),
                    title=str(i.title),
                    doi=str(i.doi),
                    mode=str(i.mode),
                    bibtex=str(i.bibtex) if hasattr(i, "bibtex") else None,
                    screenedDecision=str(i.decision),
                    finalDecision=(
                        str(i.final_decision) if hasattr(i, "final_decision") else None
                    ),
                    exclusionCriteria=str(i.exclusion_criteria),
                    reviewerCount=int(i.reviewer_count),
                    datasetID=self.dataset.DatasetID,
                    isShot=bool(i.is_shot),
                )
            )
        with self.db_connector.db.tx() as tx:
            self.db_connector.create_many_articles(tx, articles)

    def get_posisitve_shots(self):
        self.positiveShots = self.db_connector.get_shots(
            self.project_id,
            self.config["configurations"]["shots"]["positive"],
            positive=True,
        )
        pshots = []
        for j in self.positiveShots:
            tmp = {}
            for i in self.config["configurations"]["features"]:
                tmp[i] = getattr(j, i.title())
            pshots.append(tmp)
        self.positiveShots = pshots
        return self.positiveShots

    def get_negative_shots(self):
        self.negativeShots = self.db_connector.get_shots(
            self.project_id,
            self.config["configurations"]["shots"]["negative"],
            positive=False,
        )
        nshots = []
        for j in self.negativeShots:
            tmp = {}
            for i in self.config["configurations"]["features"]:
                tmp[i] = getattr(j, i.title())
            nshots.append(tmp)
        self.negativeShots = nshots
        return self.negativeShots

    def get_articles(self, retries=None):
        # get all the articles
        self.articles, self.error_decisions = self.db_connector.get_task_articles(
            self.project_id, retries=retries
        )
        return self.articles, self.error_decisions

    def get_trainable_datapath(self):
        return os.path.join(self.data_dir, f"{self.config['dataset']['name']}.csv")

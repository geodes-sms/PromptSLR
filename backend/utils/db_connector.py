import datetime
import json
import random
from prisma import Prisma
from prisma.errors import FieldNotFoundError
from hashlib import sha256


class DBConnector:
    def __init__(self):
        self.db = Prisma()
        self.db.connect()

    def __del__(self):
        self.db.disconnect()

    def connect(self):
        self.db.connect()

    def disconnect(self):
        self.db.disconnect()

    def create_user(self, email: str, password: str, username: str = None):
        user = self.db.users.create(
            {
                "Username": username or email,
                "Email": email,
                "PasswordHash": sha256(password.encode()).hexdigest(),
                "CreatedAt": datetime.now(),
            }
        )
        return user

    def create_project(
        self, projectID: str, name: str, topicTitle: str, topicDescription: str = None
    ):
        project = self.db.projects.create(
            {
                "ProjectID": projectID,
                "Name": name,
                "TopicTitle": topicTitle,
                "TopicDescription": topicDescription,
            }
        )
        return project

    def create_llm(
        self,
        projectID: str,
        name: str,
        url: str = None,
        apikey: str = None,
        defaultTemperature: float = None,
        defaultMaxTokens: int = None,
    ):
        llm = self.db.llms.create(
            {
                "ProjectID": projectID,
                "Name": name,
                "URL": url,
                "APIKey": apikey,
                "DefaultTemperature": defaultTemperature,
                "DefaultMaxTokens": defaultMaxTokens,
            }
        )
        return llm

    def create_llmhyparams(self, llmID: int, key: str, value: str):
        llmhyparams = self.db.llmhyperparams.create(
            {
                "LLMID": llmID,
                "Key": key,
                "Value": value,
            }
        )
        return llmhyparams

    def create_dataset(self, name: str, projectID: str = None):
        dataset = self.db.dataset.create(
            {
                "Name": name,
            }
        )
        return dataset

    def create_configurations(self, projectID: str, config: dict):
        configurations = self.db.configurations.create(
            {
                "ProjectID": projectID,
                "ConfigJson": json.dumps(config),
            }
        )

    def create_article(
        self,
        tx,
        key: str,
        title: str,
        doi: str,
        screenedDecision: str,
        datasetID: str,
        abstract: str = None,
        authors: str = None,
        bibtex: str = None,
        exclusionCriteria: str = None,
        inclusionCriteria: str = None,
        finalDecision: str = None,
        mode: str = None,
        keywords: str = None,
        references: str = None,
        reviewerCount: int = None,
        venue: str = None,
    ):
        articles = tx.articles.create(
            {
                "BibtexKey": key,
                "Title": title,
                "Abstract": abstract,
                "DOI": doi,
                "Authors": authors,
                "Bibtex": bibtex,
                "DatasetID": datasetID,
                "ExclusionCriteria": exclusionCriteria,
                "InclusionCriteria": inclusionCriteria,
                "FinalDecision": finalDecision,
                "Mode": mode,
                "Keywords": keywords,
                "References": references,
                "ReviewerCount": reviewerCount,
                "ScreenedDecision": screenedDecision,
                "Venue": venue,
            }
        )
        return articles

    def create_many_articles(self, articles: list):
        self.db.articles.create_many(articles)

    def create_llmdecision(
        self,
        artileKey: str,
        decision: str,
        projectID: str,
        error: str,
        retries: int,
        rawOutput: str = None,
        reason: str = None,
        confidence: float = None,
    ):
        if not self.is_decision_exists(projectID, artileKey):
            llmdecision = self.db.llmdecisions.create(
                {
                    "LLMID": self.get_llmid(projectID),
                    "ArticleKey": artileKey,
                    "ProjectID": projectID,
                    "Decision": decision,
                    "Error": error,
                    "Retries": retries,
                    "RawOutput": rawOutput,
                    "Reason": reason,
                    "Confidence": confidence,
                }
            )
        else:
            llmdecision = self.db.llmdecisions.update(
                where={
                    "ProjectID": projectID,
                    "ArticleKey": artileKey,
                },
                data={
                    "Decision": decision,
                    "Error": error,
                    "Retries": retries,
                    "RawOutput": rawOutput,
                    "Reason": reason,
                    "Confidence": confidence,
                },
            )
        return llmdecision

    def create_project_dataset(self, projectID: str, datasetID: str):
        project_dataset = self.db.projectdatasets.create(
            {
                "ProjectID": projectID,
                "DatasetID": datasetID,
            }
        )
        return project_dataset

    def run_query(self, query: str):
        result = self.db.execute_raw(query)
        return result

    def get_configurations(self, projectID: str):
        configurations = self.db.configurations.find_many(
            where={
                "ProjectID": projectID,
            }
        )
        return configurations

    def get_articles(self, datasetID: str):
        articles = self.db.articles.find_many(
            where={
                "DatasetID": datasetID,
            }
        )
        return articles

    def get_llmdecisions(self, projectID: str):
        llmdecisions = self.db.llmdecisions.find_many(
            where={
                "ProjectID": projectID,
            }
        )
        return llmdecisions

    def get_llmid(self, projectID: str):
        llm = self.db.llms.find_first(
            where={
                "ProjectID": projectID,
            }
        )
        return llm.LLMID

    def get_datasetid(self, name: str):
        dataset = self.db.dataset.find_first(
            where={
                "Name": name,
            }
        )
        return dataset.DatasetID

    def get_datasetid_by_project(self, projectID: str):
        dataset = self.db.projectdatasets.find_first(
            where={
                "ProjectID": projectID,
            }
        )
        return dataset.DatasetID

    def get_project_status(self, projectID: str):
        decision_tables = self.db.llmdecisions.find_many(
            where={
                "ProjectID": projectID,
            },
            distinct=["LLMID"],
        )
        datasetID = self.get_datasetid(projectID)
        total_articles = self.db.articles.count(
            where={
                "DatasetID": datasetID,
            }
        )
        articles_with_decision = self.db.llmdecisions.count(
            where={
                "ProjectID": projectID,
                "Decision": {"not": "error"},
            }
        )
        return total_articles, articles_with_decision

    def get_shots(self, projectID: str, count: int, positive: bool = True):
        d_id = self.get_datasetid_by_project(projectID)
        articles = self.db.articles.find_many(
            where={
                "DatasetID": d_id,
                "ScreenedDecision": ("Included" if positive else "Excluded"),
            }
        )
        articles = random.sample(articles, count)
        for article in articles:
            self.db.projectshots.create(
                {
                    "ProjectID": projectID,
                    "ArticleKey": article.Key,
                    "positive": positive,
                }
            )
        return articles

    def get_task_articles(self, projectID: str, retries: int = None):
        shots = self.db.projectshots.find_many(
            where={
                "ProjectID": projectID,
            }
        )
        datasetID = self.get_datasetid_by_project(projectID)
        articles = self.db.articles.find_many(
            where={
                "DatasetID": datasetID,
                "Key": {"not_in": [shot.ArticleKey for shot in shots]},
            }
        )
        return articles

    def get_projects(self):
        projects = self.db.projects.find_many()
        resp = {}
        for project in projects:
            resp[project.ProjectID] = project.Name
        return resp

    def is_project_exists(self, projectID: str) -> bool:
        try:
            project = self.db.projects.find_first(
                where={
                    "ProjectID": projectID,
                }
            )
            print(project)
        except FieldNotFoundError as e:
            print(e)
            return False
        return project is not None

    def is_dataset_exists(self, name: str) -> bool:

        try:
            dataset = self.db.dataset.find_first(
                where={
                    "Name": name,
                }
            )
        except FieldNotFoundError:
            return False

        print(dataset)
        return dataset is not None

    def is_decision_exists(self, projectID: str, articleKey: str) -> bool:
        decision = self.db.llmdecisions.find_first(
            where={
                "ProjectID": projectID,
                "ArticleKey": articleKey,
            }
        )
        return decision is not None

    def is_error_present(self, projectID: str) -> bool:
        # TODO: Fix for excluding fixed errors
        decision = self.db.llmdecisions.find_first(
            where={
                "ProjectID": projectID,
                "Error": True,
            }
        )
        return decision is not None

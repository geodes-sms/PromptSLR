import asyncio
import datetime
from prisma import Prisma
from hashlib import sha256


class DBConnector:
    def __init__(self):
        self.db = Prisma()

    async def connect(self):
        await self.db.connect()

    async def disconnect(self):
        await self.db.disconnect()

    async def create_user(self, email: str, password: str, username: str = None):
        user = await self.db.users.create(
            {
                "Username": username or email,
                "Email": email,
                "PasswordHash": sha256(password.encode()).hexdigest(),
                "CreatedAt": datetime.now(),
            }
        )
        return user

    async def create_project(
        self, name: str, topicTitle: str, topicDescription: str = None
    ):
        project = await self.db.projects.create(
            {
                "Name": name,
                "TopicTitle": topicTitle,
                "TopicDescription": topicDescription,
            }
        )
        return project

    async def create_llm(
        self,
        projectID: str,
        name: str,
        url: str = None,
        apikey: str = None,
        defaultTemperature: float = None,
        defaultMaxTokens: int = None,
    ):
        llm = await self.db.llms.create(
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

    async def create_llmhyparams(self, llmID: str, key: str, value: str):
        llmhyparams = await self.db.llmhyperparams.create(
            {
                "LLMID": llmID,
                "Key": key,
                "Value": value,
            }
        )
        return llmhyparams

    async def create_dataset(self, name: str, projectID: str = None):
        dataset = await self.db.datasets.create(
            {
                "Name": name,
                "ProjectID": projectID,
            }
        )
        return dataset

    async def create_configurations(self, projectID: str, config: dict):
        configurations = await self.db.configurations.create(
            {
                "ProjectID": projectID,
                "ConfigJson": config,
            }
        )

    async def create_articles(
        self,
        key: str,
        title: str,
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
        articles = await self.db.articles.create(
            {
                "Key": key,
                "Title": title,
                "Abstract": abstract,
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

    async def create_llmdecision(
        self,
        llmID: str,
        artileKey: str,
        decision: str,
        projectID: str,
        error: str,
        retries: int,
        rawOutput: str = None,
        reason: str = None,
        confidence: float = None,
    ):
        llmdecision = await self.db.llmdecisions.create(
            {
                "LLMID": llmID,
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
        return llmdecision

    async def run_query(self, query: str):
        result = await self.db.execute_raw(query)
        return result

    async def get_configurations(self, projectID: str):
        configurations = await self.db.configurations.find_many(
            {
                "where": {
                    "ProjectID": projectID,
                }
            }
        )
        return configurations

    async def get_articles(self, datasetID: str):
        articles = await self.db.articles.find_many(
            {
                "where": {
                    "DatasetID": datasetID,
                }
            }
        )
        return articles

    async def get_llmdecisions(self, projectID: str):
        llmdecisions = await self.db.llmdecisions.find_many(
            {
                "where": {
                    "ProjectID": projectID,
                }
            }
        )
        return llmdecisions

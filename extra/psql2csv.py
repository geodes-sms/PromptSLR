import pandas as pd
from utils.db_connector import DBConnector
from utils.results import Results

db = DBConnector()

project_ids = db.db.projects.find_many()
dfs = []

for project_id in project_ids:
    try:
        results = Results(project_id.ProjectID)
        df = results.get_moment_values_df()
        df["ProjectID"] = project_id.ProjectID
        df["ProjectName"] = project_id.Name
        dfs.append(df)
    except ZeroDivisionError:
        print(f"Error: {project_id}")
        continue


df = pd.concat(dfs)

df.reindex(
    columns=[
        "ProjectName",
        "completed_articles",
        "iterations",
        "articles_with_error",
        "true_positive",
        "false_positive",
        "true_negative",
        "false_negative",
        "accuracy",
        "precision",
        "recall",
        "f1_score",
        "specificity",
        "mcc",
        "balanced_accuracy",
        "miss_rate",
        "f2_score",
        "wss",
        "wss@95",
        "npv",
        "g_mean",
        "general_performance_score",
        "ProjectID",
    ]
)
df.to_csv("results-dump-2.csv", index=False)

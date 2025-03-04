import pandas as pd
from utils.db_connector import DBConnector

db = DBConnector()
project_names = [
    "Std-U0-Cy-Rn-EXn-INn-A-SH0-EXPn-RL4SE-FINAL",
    "Std-U1-Cy-Rn-EXn-INn-A-SH0-EXPn-RL4SE-FINAL",
    "Std-U2-Cy-Rn-EXn-INn-A-SH0-EXPn-RL4SE-FINAL",
    "Std-U3-Cy-Rn-EXn-INn-A-SH0-EXPn-RL4SE-FINAL",
]
project_ids = db.db.projects.find_many(where={"Name": {"in": project_names}})
projects = {}
for project_id in project_ids:
    projects[project_id.Name] = project_id.ProjectID


dfs = {}

for project_name, project_id in projects.items():
    decisoins = db.db.llmdecisions.find_many(where={"ProjectID": project_id})
    decisoins = [d.model_dump() for d in decisoins]
    dfs[project_name] = pd.DataFrame(decisoins)

from utils.db_connector import DBConnector
import pandas as pd
import json


def fetch_results_for_EASE():
    db = DBConnector()
    df = pd.read_csv("data/gamese_golden.csv", sep="\t")
    project_id = db.run_query(
        """select "ProjectID" from "Projects" where "Name"='Std-U2-Cy-Rn-EXn-INn-A-SH0-EXPn-RQy-COT-GAMESEFINAL-FINAL-GPT-4-TURBO';"""
    )[0]["ProjectID"]
    print(project_id)
    articles = db.get_articles(db.get_datasetid_by_project(project_id))
    llmdecisions = db.get_llmdecisions(projectID=project_id)
    keys = [
        29,
        62,
        65,
        98,
        106,
        133,
        190,
        237,
        260,
        273,
        293,
        340,
        358,
        381,
        422,
        560,
        577,
        583,
        587,
        607,
    ]
    final_keys = []
    for key in keys:
        for article in articles:
            if int(article.BibtexKey) == int(key):
                final_keys.append(article.Key)
                print(article.BibtexKey, article.Key)
                break

    for d in llmdecisions:
        if d.ArticleKey in final_keys:
            print(
                (
                    "IN"
                    if "include" in json.loads(d.RawOutput)["decision"].lower()
                    else "EX"
                )
            )
            # print(d.Confidence)


if __name__ == "__main__":
    fetch_results_for_EASE()

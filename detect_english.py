import pandas as pd
from langdetect import detect
import os


def is_english_text(text):
    try:
        if detect(text) == "en":
            return True
        else:
            return False
    except:
        return True


for file in os.listdir("data/bibtex"):
    if file.endswith(".csv"):
        print(file)
        print("\n")
        df = pd.read_csv("data/bibtex/" + file, sep="\t")
        print(df.columns)
        df["is_english"] = df["title"].apply(is_english_text)
        df["is_english_abstract"] = df["abstract"].apply(is_english_text)
        df["is_english_bibtex"] = df["bibtex"].apply(is_english_text)
        df["is_english"] = (
            df["is_english"] | df["is_english_abstract"] | df["is_english_bibtex"]
        )
        df = df.drop(columns=["is_english_bibtex"])
        df = df.drop(columns=["is_english_abstract"])
        print(df["is_english"].value_counts().to_dict())
        print("\n")
        print(df[df["is_english"] == False])
        print("\n")
        df = df[df["is_english"]]
        df = df.drop(columns=["is_english"])
        if not os.path.exists("data/bibtex/processed"):
            os.makedirs("data/bibtex/processed")
        df.to_csv("data/bibtex/processed/" + file, index=False, sep="\t")

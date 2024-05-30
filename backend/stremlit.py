import os
from uuid import uuid4
import pandas as pd
import streamlit as st

from utils.db_connector import DBConnector
from utils.experiments import Experiments
from utils.results import Results


st.set_page_config(page_title="PromptSLR", page_icon=":robot:", layout="wide")
st.title("PromptSLR")

data = {}
trainable_Algos = {
    "Logistic Regression": "lr",
    "Random Forest": "rf",
    "SVM": "svm",
    "Multi Naive Bayes": "mnb",
    "Complement Naive Bayes": "cnb",
}
db_instance = DBConnector()

if "key_value_pairs" not in st.session_state:
    st.session_state.key_value_pairs = []

if "pos_selection_criteria" not in st.session_state:
    st.session_state.pos_selection_criteria = []
if "neg_selection_criteria" not in st.session_state:
    st.session_state.neg_selection_criteria = []


def add_pos_selection_criteria():
    st.session_state.pos_selection_criteria.append("")


def delete_pos_selection_criteria(index):
    st.session_state.pos_selection_criteria.pop(index)


def add_neg_selection_criteria():
    st.session_state.neg_selection_criteria.append("")


def delete_neg_selection_criteria(index):
    st.session_state.neg_selection_criteria.pop(index)


def add_pair():
    st.session_state.key_value_pairs.append({"key": "", "value": ""})


def delete_pair(index):
    st.session_state.key_value_pairs.pop(index)


col1, col2, col3 = st.columns([2, 3, 2])

with col1:
    data["llm"] = {}
    st.title("LLM Configurations")
    name = st.text_input("Name", "Experiment 1")
    title = st.text_input("Title", "RL4SE")
    description = st.text_area(
        "Description", "Reinforcement Learning for Software Engineering"
    )
    data["project"] = {
        "name": name,
        "topic": {"title": title, "description": description},
    }

    llm_name = st.selectbox(
        "LLM Name", ["ChatGPT", "Trainable", "Random", "Llamafile"], key="llm_name"
    )
    if llm_name == "Trainable":
        llm_algo = st.selectbox(
            "Algorithm",
            [
                "Logistic Regression",
                "Random Forest",
                "SVM",
                "Multi Naive Bayes",
                "Complement Naive Bayes",
            ],
        )
        seed = int(st.text_input("Seed", "42"))
        fold_count = int(st.text_input("Fold Count", "5"))
        epoch = int(st.text_input("Epoch", "10"))
        add_params = {"seed": seed, "fold_count": fold_count, "epoch": epoch}
        default_params = {"temperature": None, "maxTokens": None}
        url = None
        api_key = None
    elif llm_name == "Llamafile":
        url = st.text_input("URL")
        temp = float(st.text_input("Temprature", "0.1"))
        max_token = int(st.text_input("Max Tokens", "100"))
        st.subheader("Additional Parameters")
        # Button to add a new key-value pair
        if st.button("Add"):
            add_pair()

        # Display key-value pairs dynamically
        for index, pair in enumerate(st.session_state.key_value_pairs):
            cols = st.columns(3)
            with cols[0]:
                st.session_state.key_value_pairs[index]["key"] = st.text_input(
                    f"Key {index + 1}", value=pair["key"], key=f"key_{index}"
                )
            with cols[1]:
                st.session_state.key_value_pairs[index]["value"] = st.text_input(
                    f"Value {index + 1}", value=pair["value"], key=f"value_{index}"
                )
            with cols[2]:
                if st.button(f"Delete {index + 1}", key=f"delete_{index}"):
                    delete_pair(index)
        add_params = {
            pair["key"]: pair["value"]
            for pair in st.session_state.key_value_pairs
            if pair["key"]
        }
        default_params = {"temperature": temp, "maxTokens": max_token}
        api_key = None

    elif llm_name == "ChatGPT":
        api_key = st.text_input("api_key")
        temp = st.text_input("Temprature", "0.1")
        max_token = st.text_input("Max Tokens", "100")
        st.subheader("Additional Parameters")
        # Button to add a new key-value pair
        if st.button("Add"):
            add_pair()

        # Display key-value pairs dynamically
        for index, pair in enumerate(st.session_state.key_value_pairs):
            cols = st.columns(3)
            with cols[0]:
                st.session_state.key_value_pairs[index]["key"] = st.text_input(
                    f"Key {index + 1}", value=pair["key"], key=f"key_{index}"
                )
            with cols[1]:
                st.session_state.key_value_pairs[index]["value"] = st.text_input(
                    f"Value {index + 1}", value=pair["value"], key=f"value_{index}"
                )
            with cols[2]:
                if st.button(f"Delete {index + 1}", key=f"delete_{index}"):
                    delete_pair(index)
        add_params = {
            pair["key"]: pair["value"]
            for pair in st.session_state.key_value_pairs
            if pair["key"]
        }
        default_params = {"temperature": temp, "maxTokens": max_token}
        data["llm"]["apikey"] = api_key or None
        url = None

    elif llm_name == "Random":
        seed = int(st.text_input("Seed", "42"))
        add_params = {"seed": seed}
        default_params = {"temperature": None, "maxTokens": None}
        url = None
        api_key = None

    data["llm"] = {
        "name": (
            trainable_Algos[llm_algo] if llm_name == "Trainable" else llm_name.lower()
        ),
        "url": url or None,
        "apikey": api_key or None,
        "hyperparams": {
            "isTrainable": llm_name == "Trainable",
            "additional": add_params,
            "default": default_params,
        },
    }


with col2:
    st.title("Dataset Configurations")
    ds = os.listdir("data")
    ds_name = [d.split(".")[0].upper() for d in ds]
    dataset = st.selectbox("Dataset", ds_name, key="dataset")
    if dataset in ds_name:
        st.write("Preview RL4SE Dataset")
        df = pd.read_csv(
            f"data/{dataset.lower()}.csv",
            sep="\t",
            na_values=[None],
            keep_default_na=False,
        )
        st.dataframe(df.head(10))
    else:
        st.write("No dataset selected")

    data["dataset"] = {"name": dataset.lower()}

    st.title("Experiment Configurations")
    st.subheader("Features")
    features = st.multiselect(
        "Features",
        df.drop(columns=["decision"]).columns.str.capitalize(),
        key="features",
    )
    st.subheader("Shots")
    positive_shots = st.slider("Positive Shots", 1, 10, 2, key="positive_shots")
    negative_shots = st.slider("Negative Shots", 1, 10, 2, key="negative_shots")

    st.subheader("Selection Criteria")
    st.subheader("Inclusion")
    # Button to add a new selection criteria
    pos_choose = st.radio("Choose", ["any", "all"], key="pos_choose")
    if st.button("Add Inclusion Criteria"):
        add_pos_selection_criteria()

    # Display selection criteria dynamically
    for index, criteria in enumerate(st.session_state.pos_selection_criteria):
        st.session_state.pos_selection_criteria[index] = st.text_input(
            f"Positive {index + 1}", value=criteria, key=f"pos_{index}"
        )
        if st.button(f"Delete Positive {index + 1}", key=f"delete_pos_{index}"):
            delete_pos_selection_criteria(index)

    st.subheader("Exclusion")
    neg_choose = st.radio("Choose", ["any", "all"], key="neg_choose")
    # Button to add a new selection criteria
    if st.button("Add Ecxlusion Criteria"):
        add_neg_selection_criteria()

    # Display selection criteria dynamically
    for index, criteria in enumerate(st.session_state.neg_selection_criteria):
        st.session_state.neg_selection_criteria[index] = st.text_input(
            f"Negative {index + 1}", value=criteria, key=f"neg_{index}"
        )
        if st.button(f"Delete Negative {index + 1}", key=f"delete_neg_{index}"):
            delete_neg_selection_criteria(index)

    st.subheader("Output")
    output = int(st.text_input("Classes", "3", key="output"))
    reason = st.checkbox("Reason", key="reason")
    confidence = st.checkbox("Confidence", key="confidence")

    linient = st.checkbox("Linient", key="linient")

    data["configurations"] = {
        "features": features,
        "shots": {"positive": positive_shots, "negative": negative_shots},
        "selection": {
            "positive": {
                "condition": [pos_choose],
                "criteria": st.session_state.pos_selection_criteria,
            },
            "negative": {
                "condition": [neg_choose],
                "criteria": st.session_state.neg_selection_criteria,
            },
        },
        "output": {"classes": output, "reasoning": reason, "confidence": confidence},
        "linient": linient,
    }

    if st.button("Run Experiment"):
        st.write("Running experiment...")
        bar = st.progress(0)
        project_id = str(uuid4())
        # initdb and initexperiment
        print(data)
        print(project_id)
        exp = Experiments(project_id, data, bar)
        exp.init()
        bar.progress(100)
        with col3:
            st.title("Results")
            st.write("Project ID: ", project_id)
            if not db_instance.is_project_exists(project_id):
                st.error("Experiment not found")
            r = Results(project_id)
            for k, v in r.get_results().items():
                st.write(f"{k.capitalize()}: {v}")

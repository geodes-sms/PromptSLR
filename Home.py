import json
import os
from uuid import uuid4
import pandas as pd
import streamlit as st

from utils.db_connector import DBConnector
from utils.experiments import Experiments
from utils.results import Results


st.set_page_config(
    page_title="PromptSLR",
    page_icon="🤖",
    layout="wide",
)
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


def add_pos_selection_criteria(value=""):
    st.session_state.pos_selection_criteria.append(value)


def delete_pos_selection_criteria(index):
    st.session_state.pos_selection_criteria.pop(index)


def add_neg_selection_criteria(value=""):
    st.session_state.neg_selection_criteria.append(value)


def delete_neg_selection_criteria(index):
    st.session_state.neg_selection_criteria.pop(index)


def add_pair(key="", value=""):
    st.session_state.key_value_pairs.append({"key": key, "value": value})


def delete_pair(index):
    st.session_state.key_value_pairs.pop(index)


load_experiment = False
project_id = None
list_of_experiments = db_instance.get_projects()
if list_of_experiments:
    st.sidebar.write("Load Existing Experiment:")
    project_id = st.sidebar.selectbox(
        "Experiment Name",
        [f"{value} - {key}" for key, value in list_of_experiments.items()],
    ).split(" - ")[1]
    config = json.loads(db_instance.get_configurations(project_id))
    if st.sidebar.button("Load"):
        load_experiment = True
    if st.sidebar.button("Create New"):
        load_experiment = False
    print(project_id)
    print(config)

col1, col2, col3 = st.columns([2, 3, 2])

if load_experiment:
    with col1:
        st.title("LLM Configurations")
        name = st.text_input("Experiment Name", value=config["project"]["name"])
        title = st.text_input("SR Topic", value=config["project"]["topic"]["title"])
        iterations = st.text_input(
            "Iterations",
            value=(
                config["project"]["iterations"]
                if "iterations" in config["project"]
                else 1
            ),
        )
        description = st.text_area(
            "SR Description",
            value=(
                config["project"]["topic"]["description"]
                if "description" in config["project"]["topic"]
                else ""
            ),
        )
        data["project"] = {
            "name": name,
            "topic": {"title": title, "description": description},
            "iterations": iterations,
        }
        llm_names_list = ["Chatgpt", "Trainable", "Random", "Llamafile"]
        llm_name = st.selectbox(
            "Classifier Family",
            llm_names_list,
            key="llm_name",
            index=llm_names_list.index(
                config["llm"]["name"].capitalize()
                if config["llm"]["name"].capitalize()
                in ["Chatgpt", "Random", "Llamafile"]
                else "Trainable"
            ),
        )
        if llm_name == "Trainable":
            llm_algos_list = [
                "Logistic Regression",
                "Random Forest",
                "SVM",
                "Multi Naive Bayes",
                "Complement Naive Bayes",
            ]
            if config["llm"]["name"] == "Trainable":
                index = llm_algos_list.index(
                    [
                        k
                        for k, v in trainable_Algos.items()
                        if v == config["llm"]["name"]
                    ][0]
                )
            else:
                index = 0
            llm_algo = st.selectbox(
                "Classifier Name",
                llm_algos_list,
                index=index,
            )

            seed = int(
                st.text_input(
                    "Seed", value=config["llm"]["hyperparams"]["additional"]["seed"]
                )
            )
            fold_count = int(
                st.text_input(
                    "Fold Count",
                    value=(
                        config["llm"]["hyperparams"]["additional"]["fold_count"]
                        if "fold_count" in config["llm"]["hyperparams"]["additional"]
                        else 5
                    ),
                )
            )
            epoch = int(
                st.text_input(
                    "Epoch",
                    value=(
                        config["llm"]["hyperparams"]["additional"]["epoch"]
                        if "epoch" in config["llm"]["hyperparams"]["additional"]
                        else 10
                    ),
                )
            )
            add_params = {"seed": seed, "fold_count": fold_count, "epoch": epoch}
            default_params = {"temperature": None, "maxTokens": None}
            url = None
            api_key = None
        elif llm_name == "Llamafile":
            url = st.text_input("URL", value=config["llm"]["url"])
            temp = float(
                st.text_input(
                    "Temprature",
                    value=config["llm"]["hyperparams"]["default"]["temperature"],
                )
            )
            max_token = int(
                st.text_input(
                    "Max Tokens",
                    value=config["llm"]["hyperparams"]["default"]["maxTokens"],
                )
            )
            st.subheader("Additional Parameters")
            # Button to add a new key-value pair
            if "additional" in config["llm"]["hyperparams"]:
                for key, value in config["llm"]["hyperparams"]["additional"].items():
                    add_pair(key, value)
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

        elif llm_name == "Chatgpt":
            api_key = st.text_input("api_key", value=config["llm"]["apikey"])
            temp = st.text_input(
                "Temprature",
                value=config["llm"]["hyperparams"]["default"]["temperature"],
            )
            max_token = st.text_input(
                "Max Tokens", value=config["llm"]["hyperparams"]["default"]["maxTokens"]
            )
            st.subheader("Additional Parameters")

            if "additional" in config["llm"]["hyperparams"]:
                for key, value in config["llm"]["hyperparams"]["additional"].items():
                    add_pair(key, value)
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
            seed = int(
                st.text_input(
                    "Seed", value=config["llm"]["hyperparams"]["additional"]["seed"]
                )
            )
            add_params = {"seed": seed}
            default_params = {"temperature": None, "maxTokens": None}
            url = None
            api_key = None

        data["llm"] = {
            "name": (
                trainable_Algos[llm_algo]
                if llm_name == "Trainable"
                else llm_name.lower()
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
        dataset = st.selectbox(
            "Dataset",
            ds_name,
            key="dataset",
            index=ds_name.index(config["dataset"]["name"].upper()),
        )
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
            default=[i.capitalize() for i in config["configurations"]["features"]],
        )
        st.subheader("Shots")
        positive_shots = st.slider(
            "Positive Shots",
            0,
            10,
            key="positive_shots",
            value=config["configurations"]["shots"]["positive"],
        )
        negative_shots = st.slider(
            "Negative Shots",
            0,
            10,
            key="negative_shots",
            value=config["configurations"]["shots"]["negative"],
        )

        st.subheader("Selection Criteria")
        st.subheader("Inclusion")
        # Button to add a new selection criteria
        pos_choose = st.radio(
            "Choose",
            ["any", "all"],
            key="pos_choose",
            index=["any", "all"].index(
                config["configurations"]["selectionCriteria"]["inclusion"]["condition"][
                    0
                ]
                if "selectionCriteria" in config["configurations"]
                else "any"
            ),
        )
        if "selectionCriteria" in config["configurations"]:
            for criteria in config["configurations"]["selectionCriteria"]["inclusion"][
                "criteria"
            ]:
                add_pos_selection_criteria(criteria)
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
        neg_choose = st.radio(
            "Choose",
            ["any", "all"],
            key="neg_choose",
            index=["any", "all"].index(
                config["configurations"]["selectionCriteria"]["exclusion"]["condition"][
                    0
                ]
                if "selectionCriteria" in config["configurations"]
                else "any"
            ),
        )
        # Button to add a new selection criteria
        if "selectionCriteria" in config["configurations"]:
            for criteria in config["configurations"]["selectionCriteria"]["exclusion"][
                "criteria"
            ]:
                add_neg_selection_criteria(criteria)
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
        output = int(
            st.text_input(
                "Classes",
                value=config["configurations"]["output"]["classes"],
                key="output",
            )
        )
        reason = st.checkbox(
            "Reason",
            key="reason",
            value=(
                config["configurations"]["output"]["reasoning"]
                if "reasoning" in config["configurations"]
                else False
            ),
        )
        confidence = st.checkbox(
            "Confidence",
            key="confidence",
            value=(
                config["configurations"]["output"]["confidence"]
                if "confidence" in config["configurations"]
                else False
            ),
        )

        linient = st.checkbox(
            "Linient", key="linient", value=config["configurations"]["linient"]
        )

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
            "output": {
                "classes": output,
                "reasoning": reason,
                "confidence": confidence,
            },
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
            if not db_instance.is_project_exists(project_id):
                st.error("Experiment not found")
            r = Results(project_id)
            for k, v in r.get_results().items():
                st.write(f"{' '.join(k.split('_')).capitalize()}: {v}")

else:
    with col1:
        data["llm"] = {}
        st.title("LLM Configurations")
        name = st.text_input("Experiment Name", "Experiment 1")
        title = st.text_input("SR Topic", "RL4SE")
        description = st.text_area(
            "SR Description", "Reinforcement Learning for Software Engineering"
        )
        iterations = st.text_input(
            "Iterations",
            value=1,
        )
        data["project"] = {
            "name": name,
            "topic": {"title": title, "description": description},
            "iterations": iterations,
        }

        llm_name = st.selectbox(
            "Classifier Family",
            ["Chatgpt", "Trainable", "Random", "Llamafile"],
            key="llm_name",
        )
        if llm_name == "Trainable":
            llm_algo = st.selectbox(
                "Classifier Name",
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

        elif llm_name == "Chatgpt":
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
                trainable_Algos[llm_algo]
                if llm_name == "Trainable"
                else llm_name.lower()
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
        positive_shots = st.slider("Positive Shots", 0, 10, 2, key="positive_shots")
        negative_shots = st.slider("Negative Shots", 0, 10, 2, key="negative_shots")

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
            "output": {
                "classes": output,
                "reasoning": reason,
                "confidence": confidence,
            },
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
                if not db_instance.is_project_exists(project_id):
                    st.error("Experiment not found")
                r = Results(project_id)
                for k, v in r.get_results().items():
                    st.write(f"{' '.join(k.split('_')).capitalize()}: {v}")

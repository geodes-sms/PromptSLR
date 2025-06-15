import argparse
import os
import pandas as pd
from uuid import uuid4
from utils.experiments import Experiments
from project_data_tmp import criteria, dataset_info
from dotenv import load_dotenv

load_dotenv()

exp_not_required = [
    "Std-U2-Cy-Rn-EXn-INn-A-SH1-EXPn-RQy-SIMPLE-OLLAMA-FINAL-LC-FINAL-LLAMAFILE",
    "Std-U2-Cy-Rn-EXn-INn-A-SH1-EXPn-RQn-SIMPLE-OLLAMA-FINAL-LC-FINAL-LLAMAFILE",
    "Std-U2-Cy-Rn-EXn-INn-A-SH0-EXPn-RQn-SIMPLE-OLLAMA-FINAL-LC-FINAL-LLAMAFILE",
]


def extract_shots_from_prefix(experiment_prefix):
    """Extract shot count from the experiment prefix."""
    if "SH" in experiment_prefix:
        shot_value = experiment_prefix.split("SH")[1].split("-")[0]
        shot_count = int(shot_value) if shot_value.isdigit() else 0
        return shot_count
    return 0


def run_experiment(
    data, dataset_name, experiment_prefix, template_name="lc/lc_simple.jinja"
):
    # Modify the prefix to use U0, Cy, Rn as required
    modified_prefix = (
        experiment_prefix.replace("Ux", "U0").replace("Cx", "Cy").replace("Rx", "Rn")
    )
    full_experiment_name = f"{modified_prefix}-{dataset_name.split('_')[0].upper()}-FINAL-{data['llm']['name'].upper()}"
    data["project"]["name"] = full_experiment_name
    data["dataset"] = {"name": dataset_name}

    # Update the project title and description based on the prefix
    if dataset_name in dataset_info:
        data["project"]["topic"]["title"] = dataset_info[dataset_name]["title"]

        if modified_prefix.startswith("Std"):
            data["project"]["topic"]["description"] = dataset_info[dataset_name][
                "description"
            ]

    # Set classes based on U value and confidence based on Cy
    if "U0" in experiment_prefix:
        data["configurations"]["output"]["classes"] = 2
    elif "U1" in experiment_prefix:
        data["configurations"]["output"]["classes"] = 3
    elif "U2" in experiment_prefix:
        data["configurations"]["output"]["classes"] = 4
    elif "U3" in experiment_prefix:
        data["configurations"]["output"]["classes"] = 5

    # Enable confidence if "Cy" is present
    if "Cy" in modified_prefix:
        data["configurations"]["output"]["confidence"] = True

    # Apply shot counts based on SH#
    shot_count = extract_shots_from_prefix(experiment_prefix)
    data["configurations"]["shots"]["positive"] = shot_count

    # Apply criteria based on EXy and INy in the prefix
    if "EXy" in experiment_prefix:
        if "exclusion" in criteria[dataset_name]:
            data["configurations"]["selection"]["negative"]["criteria"] = [
                f"{item}: {item}" for item in criteria[dataset_name]["exclusion"]
            ]
        else:
            print(f"Skipping {full_experiment_name}: No exclusion criteria available.")
            return

    if "INy" in experiment_prefix:
        if "inclusion" in criteria[dataset_name]:
            data["configurations"]["selection"]["positive"]["criteria"] = [
                f"{item}: {item}" for item in criteria[dataset_name]["inclusion"]
            ]
            if "AL" in experiment_prefix:
                data["configurations"]["selection"]["positive"]["condition"] = ["all"]
            if "AN" in experiment_prefix:
                data["configurations"]["selection"]["positive"]["condition"] = ["any"]
        else:
            print(f"Skipping {full_experiment_name}: No inclusion criteria available.")
            return

    print(f"Running experiment: {full_experiment_name}")
    if full_experiment_name in exp_not_required:
        print(f"Experiment {full_experiment_name} is in not required list.")
        return

    project_id = str(uuid4())
    print(f"Project ID: {project_id}")
    exp = Experiments(project_id, data, None, template_name=template_name)
    exp.init()

    print(f"Experiment {full_experiment_name} completed.")


def template_path_string_builder(dataset_name, experiment_prefix):
    """Build the template path string based on the dataset and experiment prefix."""
    dataset_name = dataset_name.split("_")[0]
    if "bibtex" in dataset_name:
        dataset_name.replace("bibtex","")


    template_path = f"final/{dataset_name}/{dataset_name}"
    if "SIMPLE" in experiment_prefix:
        template_path += "_simple"
    elif "COT" in experiment_prefix:
        template_path += "_cot"
    elif "SELECTION" in experiment_prefix:
        template_path += "_selection"

    if "RQy" in experiment_prefix:
        template_path += "_rq"

    if "SH1" in experiment_prefix:
        template_path += "_shot"

    return template_path + ".jinja"


def main():
    parser = argparse.ArgumentParser(description="Run experiments from CLI.")

    parser.add_argument(
        "--iterations", type=int, default=1, help="Number of iterations"
    )
    parser.add_argument("--llm_name", type=str, required=True, help="LLM name")
    parser.add_argument("--api_key", type=str, help="API key for LLM")
    parser.add_argument(
        "--temprature", type=float, default=float(0), help="Temperature"
    )
    parser.add_argument("--max_tokens", type=int, default=512, help="Max tokens")
    parser.add_argument("--url", type=str, help="URL for LLM")
    parser.add_argument(
        "--dataset_dir",
        type=str,
        default="data",
        help="Directory where datasets are stored",
    )
    parser.add_argument(
        "--template_name",
        type=str,
        help="Template name for the experiment",
    )

    args = parser.parse_args()

    data = {
        "project": {
            "name": "",
            "topic": {"title": "", "description": ""},
            "iterations": args.iterations,
        },
        "llm": {
            "name": args.llm_name.lower(),
            "url": args.url or None,
            "apikey": args.api_key or None,
            "hyperparams": {
                "isTrainable": False,
                "additional": {"seed": 5},
                "default": {
                    "temperature": args.temprature,
                    "maxTokens": args.max_tokens,
                },
            },
        },
    }

    datasets = [
        # "rl4se_golden",
        # "lc_golden",
        # "mobilemde_golden",
        # "mpm4cps_golden",
        # "updatecollabmde_golden",
        # "gamese_golden",
        # "esm2_golden",
        # "testnn_golden",
        #        "dtcps_golden",
        #        "trustse_golden",
        #        "behave_golden"
        # "esple_golden",
        # "secselfadapt_golden",
        # "smellreprod_golden",
       # "testnnbibtex_golden",
       # "smellreprodbibtex_golden"
        #"updatecollabmdebibtex_golden",
        #"lcbibtex_golden",
       "rl4sebibtex_golden",
        "mpm4cpsbibtex_golden"
    ]

    experiment_prefixes = [
        #        "Std-U2-Cy-Rn-EXn-INn-A-SH0-EXPn-RQy-SIMPLE-OLLAMA-FINAL1",
        #        "Std-U2-Cy-Rn-EXn-INn-A-SH1-EXPn-RQy-SIMPLE-OLLAMA-FINAL1",
        #        "Std-U2-Cy-Rn-EXn-INn-A-SH0-EXPn-RQn-SIMPLE-OLLAMA-FINAL1",
        #        "Std-U2-Cy-Rn-EXn-INn-A-SH1-EXPn-RQn-SIMPLE-OLLAMA-FINAL1",
        #        "Std-U2-Cy-Rn-EXn-INn-A-SH0-EXPn-RQy-SELECTION-OLLAMA-FINAL1",
        #        "Std-U2-Cy-Rn-EXn-INn-A-SH1-EXPn-RQy-SELECTION-OLLAMA-FINAL1",
        #        "Std-U2-Cy-Rn-EXn-INn-A-SH0-EXPn-RQy-COT-OLLAMA-FINAL1",
        #        "Std-U2-Cy-Rn-EXn-INn-A-SH1-EXPn-RQy-COT-OLLAMA-FINAL1",
        #        "Std-U2-Cy-Rn-EXn-INn-A-SH0-EXPn-RQy-COT",
        #        "Std-U2-Cy-Rn-EXn-INn-A-SH0-EXPn-RQy-SELECTION",
        #        "Std-U2-Cy-Rn-EXn-INn-A-SH0-EXPn-RQy-COT-DEEPSEEKPROMPT",
        "Std-U2-Cy-Rn-EXn-INn-A-SH0-EXPn-RQy-SELECTION-BIBTEX",
        "Std-U2-Cy-Rn-EXn-INn-A-SH0-EXPn-RQy-COT-BIBTEX",
    ]

    for dataset in datasets:
        dataset_path = os.path.join(args.dataset_dir, f"{dataset}.csv")
        if not os.path.exists(dataset_path):
            print(f"Dataset {dataset} not found at {dataset_path}")
            continue

        selected_features = ["bibtex"]  # Columns remain the same

        data["configurations"] = {
            "features": selected_features,
            "shots": {"positive": 0, "negative": 0},  # Default shot values
            "selection": {
                "positive": {"condition": ["any"], "criteria": []},
                "negative": {"condition": ["any"], "criteria": []},
            },
            "output": {"classes": 2, "reasoning": False, "confidence": False},
            "linient": True,
        }

        for prefix in experiment_prefixes:
            template_name = args.template_name or template_path_string_builder(
                dataset, prefix
            )
            print(f"Using template: {template_name}")
            run_experiment(data, dataset, prefix, template_name)


if __name__ == "__main__":
    main()

import argparse
import os
import pandas as pd
from uuid import uuid4
from utils.experiments import Experiments

dataset_info = {
    "lc_golden": {
        "title": "Domain-specific modeling language composition",
        "description": "approaches and techniques for composing heterogeneous domain-specific modeling languages",
    },
    "rl4se_golden": {
        "title": "Reinforcement learning for software engineering",
        "description": "",
    },
    "mpm4cps_golden": {
        "title": "Multi-paradigm modeling of cyber–physical systems",
        "description": "Multi-paradigm modeling approaches and applications to model cyber-physical systems",
    },
    "mobilemde_golden": {
        "title": "Modeling on mobile devices",
        "description": "model-driven engineering techniques, languages, and tools that are touch-enabled to model software on mobile devices",
    },
    "updatecollabmde_golden": {
        "title": "Collaborative modeling systematic update",
        "description": "techniques where multiple stakeholders collaborate and manage on shared models in model-driven software engineering",
    },
}


def run_experiment(data, dataset_name, experiment_prefix):
    # Construct the full experiment name
    full_experiment_name = f"{experiment_prefix}-{dataset_name.split('_')[0].upper()}"
    data["project"]["name"] = full_experiment_name
    data["dataset"] = {"name": dataset_name}

    # Update the project title and description based on the dataset
    if dataset_name in dataset_info:
        data["project"]["topic"]["title"] = dataset_info[dataset_name]["title"]
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

    if "Cy" in experiment_prefix:
        data["configurations"]["output"]["confidence"] = True

    print(f"Running experiment: {full_experiment_name}")

    project_id = str(uuid4())
    exp = Experiments(project_id, data, None)
    exp.init()

    print(f"Experiment {full_experiment_name} completed.")


def main():
    parser = argparse.ArgumentParser(description="Run experiments from CLI.")

    parser.add_argument(
        "--iterations", type=int, default=1, help="Number of iterations"
    )
    parser.add_argument("--llm_name", type=str, required=True, help="LLM name")
    parser.add_argument("--api_key", type=str, help="API key for LLM")
    parser.add_argument(
        "--dataset_dir",
        type=str,
        default="data",
        help="Directory where datasets are stored",
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
            "url": None,
            "apikey": args.api_key or None,
            "hyperparams": {
                "isTrainable": False,
                "additional": {},
                "default": {"temperature": None, "maxTokens": None},
            },
        },
    }

    datasets = [
        "rl4se_golden",
        "lc_golden",
        "mobilemde_golden",
        "mpm4cps_golden",
        "updatecollabmde_golden",
    ]

    experiment_prefixes = [
        "Std-U0-Cn-Rn-EXn-INn-A-SH0-EXPn",
        "Std-U1-Cn-Rn-EXn-INn-A-SH0-EXPn",
        "Std-U2-Cn-Rn-EXn-INn-A-SH0-EXPn",
        "Std-U3-Cn-Rn-EXn-INn-A-SH0-EXPn",
        "Std-U0-Cy-Rn-EXn-INn-A-SH0-EXPn",
        "Std-U1-Cy-Rn-EXn-INn-A-SH0-EXPn",
        "Std-U2-Cy-Rn-EXn-INn-A-SH0-EXPn",
        "Std-U3-Cy-Rn-EXn-INn-A-SH0-EXPn",
    ]

    for dataset in datasets:

        # Select only the "title" and "abstract" columns
        selected_features = ["title", "abstract"]

        data["configurations"] = {
            "features": selected_features,
            "shots": {"positive": 0, "negative": 0},  # Set all shots to zero
            "selection": {
                "positive": {"condition": ["any"], "criteria": []},
                "negative": {"condition": ["any"], "criteria": []},
            },
            "output": {"classes": 3, "reasoning": False, "confidence": False},
            "linient": True,
        }

        for prefix in experiment_prefixes:
            run_experiment(data, dataset, prefix)


if __name__ == "__main__":
    main()

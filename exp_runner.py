import argparse
import os
import pandas as pd
from uuid import uuid4
from utils.experiments import Experiments

exp_not_required = []

# Dataset information with titles and descriptions
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
    "gamese_golden": {
        "title": "The consolidation of game software engineering: A systematic literature review of software engineering for industry-scale computer games",
        "description": "This study evaluates the current state of the art in software engineering for industry-scale computer games identifying gaps and consolidating the magnitude and growth of this field.",
    },
}

# Criteria for each dataset
criteria = {
    "rl4se_golden": {
        "exclusion": [
            "E1: Does not define or use a RL method",
            "E2: Software engineering is not the problem RL is used for",
            "E3: Only conceptual results are reported",
            "E4: Published after 2022",
            "E5: Other not a paper",
        ]
    },
    "lc_golden": {
        "inclusion": [
            "The article is related to any kind of composition of DSMLs",
            "The article is related to the composition of metamodels",
            "The article is related to the composition of models",
            "The article is related to multi-paradigm modeling",
            "The article is related to the co-simulation of DSMLs",
        ],
        "exclusion": [
            "EC1: The article is related to DS(M)Ls but not their composition",
            "EC3: The article is not directly related to DS(M)Ls or to composition",
            "EC2: The article addresses the composition of non-modeling languages",
            "EC5: The article has fewer than 4 pages",
            "EC6: The article escaped automatic filters",
            "EC4: The article is not in the software engineering domain",
            "EC7: The article is a duplicate",
            "EC0: The article does not use or present a modeling language composition technique",
        ],
    },
    "mobilemde_golden": {
        "exclusion": [
            "Article is not in English",
            "Off topic",
            "It does not use modelling",
            "It does not use mobile development",
        ]
    },
    "mpm4cps_golden": {
        "inclusion": [
            "Publication date from 1/1/2006 ->",
            "Relevance with respect to research questions",
            "Explicit mentioning of modelling of cyber-physical system",
            "Papers that report a methodology, metric or formalism for modelling of CPS",
            "Analysis of relevant application domains for modelling of CPS",
        ],
        "exclusion": [
            "Informal literature and secondary/tertiary studies",
            "Duplicated papers.",
            "Papers that did not apply to research questions",
            "Papers with the same content in different paper versions",
            "Papers written in other than English language",
            "Purely hardware, or electrical engineering perspective papers",
            "Outside of the SLR date range",
        ],
    },
    "updatecollabmde_golden": {
        "exclusion": [
            "E_I1 - NOT an MDSE method; or NOT supporting collaboration of multiple stakeholders",
            "E_I2 - Models are NOT the primary artifacts within the collaboration process.",
            "E_I3 - Does NOT provide validation or evaluation of the proposed method or technique",
            "E_I4: Non-peer-reviewed",
            "E_I5: Studies NOT in English, or NOT available in full-text",
            "E1: Discusses only business processes and collaboration practices, without proposing a specific method or technique",
            "E2: Secondary studies (e.g., systematic literature reviews, surveys, etc.)",
            "E3: Tutorial papers, long abstract papers, poster papers, editorials",
        ]
    },
}


def run_experiment(data, dataset_name, experiment_prefix):
    # Modify the prefix to use U0, Cy, Rn as required
    modified_prefix = (
        experiment_prefix.replace("Ux", "U0").replace("Cx", "Cy").replace("Rx", "Rn")
    )
    full_experiment_name = (
        f"{modified_prefix}-{dataset_name.split('_')[0].upper()}-FINAL"
    )
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
                "additional": {},
                "default": {
                    "temperature": args.temprature,
                    "maxTokens": args.max_tokens,
                },
            },
        },
    }

    datasets = [
        "rl4se_golden",
        "lc_golden",
        "mobilemde_golden",
        "mpm4cps_golden",
        "updatecollabmde_golden",
        "gamese_golden",
    ]

    experiment_prefixes = [
        "Std-U0-Cy-Ry-EXn-INn-A-SH0-EXPn",
        "Std-U0-Cy-Rn-EXy-INn-A-SH0-EXPn",
        "Std-U0-Cy-Rn-EXn-INy-AN-SH0-EXPn",
        "Std-U0-Cy-Rn-EXn-INy-AL-SH0-EXPn",
    ]

    for dataset in datasets:
        dataset_path = os.path.join(args.dataset_dir, f"{dataset}.csv")
        if not os.path.exists(dataset_path):
            print(f"Dataset {dataset} not found at {dataset_path}")
            continue

        selected_features = ["title", "abstract"]  # Columns remain the same

        data["configurations"] = {
            "features": selected_features,
            "shots": {"positive": 0, "negative": 0},  # Set all shots to zero
            "selection": {
                "positive": {"condition": ["any"], "criteria": []},
                "negative": {"condition": ["any"], "criteria": []},
            },
            "output": {"classes": 2, "reasoning": False, "confidence": False},
            "linient": True,
        }

        for prefix in experiment_prefixes:
            run_experiment(data, dataset, prefix)


if __name__ == "__main__":
    main()

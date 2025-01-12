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

from typing import List, Any
from dataclasses import dataclass, field
from dataclass_wizard import JSONWizard


@dataclass
class Output:
    classes: int = field(default=2)
    reason: bool = field(default=False)
    confidence: bool = field(default=False)


@dataclass
class Clusion:
    condition: List[str]
    criteria: List[Any]


@dataclass
class SelectionCriteria:
    inclusion: Clusion | None = field(default=None)
    exclusion: Clusion | None = field(default=None)


@dataclass
class Shots:
    positive: int | None = field(default=None)
    negative: int | None = field(default=None)


@dataclass
class Configurations:
    features: List[str]
    output: Output
    linient: bool = field(default=True)
    shots: Shots | None = field(default=None)
    selection_criteria: SelectionCriteria | None = field(default=None)


@dataclass
class Dataset:
    name: str


@dataclass
class Default:
    temprature: float = field(default=0.2)
    max_tokens: int = field(default=512)


@dataclass
class Hyperparams:
    default: Default
    is_trainable: bool
    additional: List[dict] | None = field(default=None)


@dataclass
class Llm:
    name: str
    url: str
    apikey: str
    hyperparams: Hyperparams


@dataclass
class Topic:
    title: str
    description: str | None = field(default=None)


@dataclass
class Project:
    name: str
    topic: Topic


@dataclass
class JsonConfig(JSONWizard):
    project: Project
    llm: Llm
    dataset: Dataset
    configurations: Configurations

from utils.datamodel import JsonConfig
from utils.datasets import Datasets


class PromptConfig:
    def __init__(self, config, dataset: Datasets) -> None:
        self.json = config
        self.datasets = dataset
        self.data = {
            "positiveShots": (
                self.datasets.get_posisitve_shots()
                if "shots" in config["configurations"]
                else None
            ),
            "negativeShots": (
                self.datasets.get_negative_shots()
                if "shots" in config["configurations"]
                else None
            ),
        }


# if __name__ == "__main__":
#     import json

#     with open("/home/gauransh/Code/PromptSLR/backend/utils/schema/test.json", "r") as f:
#         data = json.load(f)
#     pc = PromptConfig(data)
#     print(pc)

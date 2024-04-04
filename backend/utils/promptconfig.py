from utils.datamodel import JsonConfig
from utils.datasets import Datasets


class PromptConfig:
    def __init__(self, config) -> None:
        self.json = config
        self.datasets = Datasets(config)
        self.data = {
            "positiveShots": self.datasets.get_posisitve_shots(),
            "negativeShots": self.datasets.get_negative_shots(),
        }


# if __name__ == "__main__":
#     import json

#     with open("/home/gauransh/Code/PromptSLR/backend/utils/schema/test.json", "r") as f:
#         data = json.load(f)
#     pc = PromptConfig(data)
#     print(pc)

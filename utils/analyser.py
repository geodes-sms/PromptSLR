import os
import jsonschema
import json


class ConfigurationAnalyser:
    def __init__(
        self,
        data,
        schema=None,
        schema_file=None,
    ):
        self.data = data
        if schema_file:
            with open(schema_file, "r") as file:
                self.schema = json.load(file)
        elif schema:
            self.schema = schema
        else:
            with open(
                os.path.join(
                    os.path.dirname(__file__), "schema", "configuration.schema.json"
                ),
                "r",
            ) as f:
                self.schema = json.load(f)

    def validate_data(self):
        try:
            jsonschema.validate(self.data, self.schema)
            print("Data is valid")
            return "Data is valid", True
        except jsonschema.ValidationError as e:
            print(e.message)
            return e.message, False

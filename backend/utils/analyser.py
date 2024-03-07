import jsonschema
import json


class ConfigurationAnalyser:
    def __init__(
        self,
        data,
        schema=None,
        schema_file="utils/schema/configuration.schema.json",
    ):
        self.data = data
        if schema_file:
            with open(schema_file, "r") as file:
                self.schema = json.load(file)
        elif schema:
            self.schema = schema
        else:
            raise ValueError("Schema or schema file must be provided")

    def validate_data(self):
        try:
            jsonschema.validate(self.data, self.schema)
            return True
        except jsonschema.ValidationError as e:
            return e.message

import jinja2
import os
from utils.promptconfig import PromptConfig
import tiktoken


class TemplateEngine:
    def __init__(self, template: str = None):
        self.env = jinja2.Environment(
            loader=jinja2.FileSystemLoader(
                os.path.join(os.path.dirname(__file__), "templates")
            ),
            autoescape=True,
            trim_blocks=True,
            lstrip_blocks=True,
            keep_trailing_newline=True,
        )
        self.encoder = encoding = tiktoken.get_encoding("cl100k_base")

    def render(self, promptConfig: PromptConfig, template_name: str = "default.jinja"):
        self.renderdTemplate = self.env.get_template(template_name).render(
            json=promptConfig.json, data=promptConfig.data
        )
        return self.renderdTemplate

    def get_tokens(self):
        return len(self.encoder.encode(self.renderdTemplate))

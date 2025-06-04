import json
from models.attribute import Attribute
from models.rule import Rule


class Project:
    def __init__(self, name=""):
        self.name = name
        self.attributes: list[Attribute] = []
        self.rules: list[Rule] = []

    def to_dict(self):
        return {
            "name": self.name,
            "attributes": [
                attr.to_dict() for attr in self.attributes
            ],
            "rules": [
                rule.to_dict() for rule in self.rules
            ],
        }

    def from_dict(self, data):
        self.name = data.get("name", "")
        self.attributes = [
            Attribute.from_dict(a) for a in data.get(
                "attributes", [],
            )
        ]
        self.rules = [
            Rule.from_dict(r) for r in data.get(
                "rules", [],
            )
        ]
        return self

    def save(self, filepath: str):
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(self.to_dict(), f, ensure_ascii=False, indent=2)

    def load(self, filepath: str):
        with open(filepath, encoding="utf-8") as f:
            data = json.load(f)
            self.from_dict(data)

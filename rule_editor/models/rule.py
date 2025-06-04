class Rule:
    def __init__(self, attr_id: int, value: str):
        self.attr_id = attr_id
        self.value = value

    def to_dict(self):
        return {
            "value": self.value,
            "attr_id": self.attr_id,
        }

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            data["attr_id"],
            data["value"],
        )

from enum import Enum


class BaseEnum(Enum):
    @classmethod
    def get_by_key(cls, key):
        try:
            return cls[key].value
        except KeyError:
            raise ValueError(
                f"Invalid key: {key}. Valid keys are: {list(cls.__members__.keys())}"
            )

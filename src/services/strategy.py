from src.services.factory import register


class DataStrategy:
    def process(self, data: list) -> list:
        pass


@register("encryption")
class EncryptionStrategy(DataStrategy):
    def __init__(self, key: str = "004F"):
        self.key = key

    def process(self, data: list) -> list:
        return [f"encrypted_{x}_{self.key}" for x in data]


@register("compression")
class CompressionStrategy(DataStrategy):
    def __init__(self, factor: float = 0.85):
        self.factor = factor

    def process(self, data: list) -> list:
        return [x * self.factor for x in data]

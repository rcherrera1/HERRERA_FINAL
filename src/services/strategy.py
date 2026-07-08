# In src/services/strategy.py

from src.services.factory import register

# 1. Base Strategy Interface (Optional but recommended for strict typing)
class DataStrategy:
    def process(self, data: list) -> list:
        pass

# 2. Strategy A: dynamically registered as 'encryption'
@register("encryption")
class EncryptionStrategy(DataStrategy):
    def __init__(self, key: str = "004F"):
        self.key = key

    def process(self, data: list) -> list:
        # Implement mock encryption logic here
        return [f"encrypted_{x}_{self.key}" for x in data]

# 3. Strategy B: dynamically registered as 'compression'
@register("compression")
class CompressionStrategy(DataStrategy):
    def __init__(self, factor: float = 0.85):
        self.factor = factor

    def process(self, data: list) -> list:
        # Implement mock compression logic here
        return [x * self.factor for x in data]
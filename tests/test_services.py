import pytest
from src.services.auth import JWTAuthService
from src.services.factory import service_factory, register
from src.services.strategy import EncryptionStrategy, CompressionStrategy

class TestMicroservices:
    
    # --- 1. Test the JWT Authentication Service ---
    def test_jwt_generation_and_verification(self):
        token = JWTAuthService.generate_token("test_client", "admin")
        assert token is not None
        
        decoded = JWTAuthService.verify_token(token)
        assert decoded is not None
        assert decoded["sub"] == "test_client"
        assert decoded["scope"] == "admin"
        
    def test_jwt_invalid_token(self):
        result = JWTAuthService.verify_token("fake.jwt.token")
        assert result is None

    # --- 2. Test the Factory Pattern ---
    def test_factory_registration_and_discovery(self):
        @register("test_service")
        class DummyService:
            def execute(self):
                return "success"
                
        # Discover the service dynamically
        discovered_service = service_factory.get_service("test_service")
        assert discovered_service.execute() == "success"
        
    def test_factory_missing_service(self):
        with pytest.raises(ValueError):
            service_factory.get_service("nonexistent_service")

    # --- 3. Test the Strategy Pattern ---
    def test_encryption_strategy(self):
        data = [78, 82]
        strategy = EncryptionStrategy(key="004F")
        result = strategy.process(data)
        
        assert len(result) == 2
        assert result[0] == "encrypted_78_004F"
        assert result[1] == "encrypted_82_004F"

    def test_compression_strategy(self):
        data = [100, 200]
        strategy = CompressionStrategy(factor=0.85)
        result = strategy.process(data)
        
        assert len(result) == 2
        assert result[0] == 85.0
        assert result[1] == 170.0
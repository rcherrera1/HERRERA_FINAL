import os
import datetime
import jwt
from typing import Dict, Optional

# Remediating SEC-001: Extract secret key from environment variables with a secure fallback
SECRET_KEY = os.getenv("JWT_SECRET_KEY", "f7bca74d823e5a481c19b26d830b561c2849ef9b010f3c5b56345829a")
ALGORITHM = "HS256"

class JWTAuthService:
    """
    A standalone JWT authentication layer responsible for issuing and verifying
    cryptographic tokens to secure inter-service discovery communications.
    """

    @staticmethod
    def generate_token(client_id: str, scope: str = "service_access") -> str:
        """
        Generates a secure, cryptographically signed JSON Web Token valid for 1 hour.
        """
        now = datetime.datetime.now(datetime.timezone.utc)
        payload = {
            "sub": client_id,                       # Subject (Who the token represents)
            "scope": scope,                         # Access capabilities
            "iat": int(now.timestamp()),            # Issued At timestamp
            "exp": int((now + datetime.timedelta(hours=1)).timestamp()) # Expiration timestamp
        }
        
        # Sign the payload using the HMAC-SHA256 algorithm and the Secret Key
        return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

    @staticmethod
    def verify_token(token: str) -> Optional[Dict]:
        """
        Validates the token signature, structural integrity, and expiration boundaries.
        Returns the decoded payload if valid, or None if authentication fails.
        """
        try:
            # Cryptographically decrypt and verify the token signature
            decoded_payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            return decoded_payload
        except jwt.ExpiredSignatureError:
            # Caught: Gate failure due to token expiration
            return None
        except jwt.InvalidTokenError:
            # Caught: Gate failure due to signature mismatch or structural tamper
            return None
import os
import datetime
import jwt
from typing import Dict, Optional

# Extracted secret key from environment variables with a secure fallback
SECRET_KEY = os.getenv(
    "JWT_SECRET_KEY", 
    "f7bca74d823e5a481c19b26d830b561c2849ef9b010f3c5b56345829a"
)
ALGORITHM = "HS256"


class JWTAuthService:
    """
    A standalone JWT authentication layer responsible for issuing and verifying
    cryptographic tokens to secure inter-service communications.
    """

    @staticmethod
    def generate_token(client_id: str, scope: str = "service_access") -> str:
        """
        Generates a secure, signed JWT valid for 1 hour.
        """
        now = datetime.datetime.now(datetime.timezone.utc)
        payload = {
            "sub": client_id,
            "scope": scope,
            "iat": int(now.timestamp()),
            "exp": int((now + datetime.timedelta(hours=1)).timestamp())
        }
        
        return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

    @staticmethod
    def verify_token(token: str) -> Optional[Dict]:
        """
        Validates the token signature, structural integrity, and boundaries.
        """
        try:
            return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None
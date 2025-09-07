import os
import time
from typing import Optional, Dict, Any

import httpx
import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

security = HTTPBearer(auto_error=False)

JWKS_URL = os.getenv("SUPABASE_JWKS_URL")
JWT_AUD = os.getenv("SUPABASE_JWT_AUDIENCE", "authenticated")

class JWKSCache:
    _cached_at: float = 0
    _data: Optional[Dict[str, Any]] = None
    _ttl: int = 60 * 60

    async def get(self) -> Dict[str, Any]:
        now = time.time()
        if not self._data or (now - self._cached_at) > self._ttl:
            if not JWKS_URL:
                raise RuntimeError("SUPABASE_JWKS_URL nÃ£o configurado.")
            async with httpx.AsyncClient(timeout=10) as client:
                r = await client.get(JWKS_URL)
                r.raise_for_status()
                self._data = r.json()
                self._cached_at = now
        return self._data

jwks_cache = JWKSCache()

async def get_current_user(token: HTTPAuthorizationCredentials = Depends(security)) -> Dict[str, Any]:
    if token is None or token.scheme.lower() != "bearer":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing bearer token")

    jwks = await jwks_cache.get()
    unverified = jwt.get_unverified_header(token.credentials)
    kid = unverified.get("kid")
    if not kid:
        raise HTTPException(status_code=401, detail="Invalid token header")

    k = next((k for k in jwks.get("keys", []) if k.get("kid") == kid), None)
    if not k:
        raise HTTPException(status_code=401, detail="Signing key not found")

    try:
        public_key = jwt.algorithms.RSAAlgorithm.from_jwk(k)
        claims = jwt.decode(
            token.credentials,
            public_key,
            algorithms=[k.get("alg", "RS256")],
            audience=JWT_AUD,
            options={"verify_exp": True},
        )
        return claims
    except jwt.PyJWTError as e:
        raise HTTPException(status_code=401, detail=f"Token invÃ¡lido: {e}")

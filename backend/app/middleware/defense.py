from fastapi import Request, HTTPException, status
from starlette.middleware.base import BaseHTTPMiddleware
from app.services.defense import defense_service
from app.db.session import AsyncSessionLocal
# Note: Middleware in FastAPI with async database calls can be tricky due to session management.
# For Phase 0, we will try a lightweight approach or skip global blocking for per-endpoint dependency.
# But "Watch everything" implies global.
# We will use a dependency-based approach on a high-level router or middleware if possible.

class DefenseMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # We need to know the Org ID to check if IP is blocked FOR THAT ORG.
        # But Org ID is inside the token/request data.
        # Global blocking (Blacklist) is easier.
        # Per-Org blocking requires parsing Auth first.
        
        # Strategy: Let endpoints handle it via Dependency?
        # Or, if we want to protect the whole app, we assume Global Block for now for simplicity 
        # OR we rely on the implementation in `deps` to check "Is Request IP Blocked for User's Org?".
        
        # User requirement: "Auto-block IP" which usually means specific to the attack context.
        # If I attack Org A, I might be blocked for Org A.
        
        # I will skip global middleware for now and rely on logic within `deps.get_current_user` or specific checks, 
        # OR implement a middleware that just checks "Global Blacklist" if we had one.
        # Since the roadmap says "Configurable per organization", it must be context-aware.
        
        response = await call_next(request)
        return response

# Actually, I'll implement a Dependency Component for "CheckDefense" 
# Middleware is too early because we don't know the Org yet (Auth header parsing happens later).

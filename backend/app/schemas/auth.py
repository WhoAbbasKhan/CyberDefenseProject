from pydantic import BaseModel, EmailStr
from typing import Optional, List

class GoogleLogin(BaseModel):
    token: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None
    
# Passkey Schemas
class PublicKeyCredentialCreationOptionsRequest(BaseModel):
    username: str
    display_name: str

class PublicKeyCredentialRequestOptionsRequest(BaseModel):
    username: Optional[str] = None

class RegistrationResponse(BaseModel):
    id: str
    rawId: str
    response: dict
    type: str
    clientExtensionResults: dict
    authenticatorAttachment: Optional[str] = None

class AuthenticationResponse(BaseModel):
    id: str
    rawId: str
    response: dict
    type: str
    clientExtensionResults: dict

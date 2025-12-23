from webauthn import (
    generate_registration_options,
    verify_registration_response,
    generate_authentication_options,
    verify_authentication_response,
)
from webauthn.helpers.structs import (
    AttestationConveyancePreference,
    AuthenticatorSelectionCriteria,
    UserVerificationRequirement,
    RegistrationCredential,
    AuthenticationCredential,
)
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.config import settings
from app.models.user import User
from app.models.auth_provider import AuthProvider
import json
from datetime import datetime

class WebAuthnService:
    async def _get_user_providers(self, db: AsyncSession, user_id: int):
        result = await db.execute(
            select(AuthProvider).where(
                AuthProvider.user_id == user_id, 
                AuthProvider.provider_type == "passkey"
            )
        )
        return result.scalars().all()

    async def generate_registration_options(self, user: User, db: AsyncSession):
        providers = await self._get_user_providers(db, user.id)
        exclude_credentials = []
        for p in providers:
            exclude_credentials.append({"id": p.credential_id, "type": "public-key", "transports": []})
            
        options = generate_registration_options(
            rp_id=settings.RP_ID,
            rp_name=settings.RP_NAME,
            user_id=str(user.id).encode(),
            user_name=user.email,
            user_display_name=user.full_name or user.email,
            attestation=AttestationConveyancePreference.NONE,
            authenticator_selection=AuthenticatorSelectionCriteria(
                user_verification=UserVerificationRequirement.PREFERRED
            ),
            exclude_credentials=exclude_credentials,
        )
        return options

    async def verify_registration(self, db: AsyncSession, user: User, response_data: dict, challenge: str):
        try:
            credential = RegistrationCredential.parse_raw(json.dumps(response_data))
            verification = verify_registration_response(
                credential=credential,
                expected_challenge=challenge.encode() if isinstance(challenge, str) else challenge,
                expected_origin=settings.RP_ORIGIN,
                expected_rp_id=settings.RP_ID,
            )
            
            new_provider = AuthProvider(
                user_id=user.id,
                provider_type="passkey",
                credential_id=verification.credential_id.decode('latin-1') if isinstance(verification.credential_id, bytes) else verification.credential_id,
                public_key=verification.credential_public_key,
                sign_count=verification.sign_count,
                device_name="User Device"
            )
            db.add(new_provider)
            await db.commit()
            return True, "Registration successful"
        except Exception as e:
            return False, str(e)

    async def generate_authentication_options(self, db: AsyncSession, user: User = None):
        allow_credentials = []
        if user:
            providers = await self._get_user_providers(db, user.id)
            for p in providers:
                allow_credentials.append({"id": p.credential_id, "type": "public-key", "transports": []})
        
        options = generate_authentication_options(
            rp_id=settings.RP_ID,
            user_verification=UserVerificationRequirement.PREFERRED,
            allow_credentials=allow_credentials,
        )
        return options

    async def verify_authentication(self, db: AsyncSession, response_data: dict, challenge: str, user: User):
        try:
            credential = AuthenticationCredential.parse_raw(json.dumps(response_data))
            
            result = await db.execute(
                select(AuthProvider).where(
                    AuthProvider.credential_id == credential.id,
                    AuthProvider.user_id == user.id
                )
            )
            provider = result.scalars().first()
            
            if not provider:
                raise Exception("Credential not found")

            verification = verify_authentication_response(
                credential=credential,
                expected_challenge=challenge.encode() if isinstance(challenge, str) else challenge,
                expected_origin=settings.RP_ORIGIN,
                expected_rp_id=settings.RP_ID,
                credential_public_key=provider.public_key,
                credential_current_sign_count=provider.sign_count,
            )
            
            provider.sign_count = verification.new_sign_count
            provider.last_used_at = datetime.utcnow()
            await db.commit()
            
            return True, "Authentication successful"
        except Exception as e:
            return False, str(e)

webauthn_service = WebAuthnService()

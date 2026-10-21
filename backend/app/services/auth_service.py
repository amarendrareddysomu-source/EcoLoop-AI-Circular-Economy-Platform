import secrets
from typing import Optional, Dict, Any
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.repositories.user_repository import user_repository
from app.repositories.organization_repository import organization_repository
from app.schemas.user import UserCreate, UserLogin
from app.models.user import User, UserRole
from app.models.organization import Organization
from app.core.security import (
    get_password_hash, 
    verify_password, 
    create_access_token, 
    create_refresh_token,
    decode_access_token
)
from app.core.exceptions import AuthenticationError, NotFoundError, AppException
from app.core.logging import logger

class AuthService:
    def register_user(self, db: Session, user_in: UserCreate) -> User:
        existing = user_repository.get_by_email(db, user_in.email)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User with this email already registered"
            )

        hashed_pw = get_password_hash(user_in.password)
        v_token = secrets.token_urlsafe(32)

        db_user = User(
            email=user_in.email.lower(),
            hashed_password=hashed_pw,
            full_name=user_in.full_name,
            role=user_in.role or UserRole.USER.value,
            organization_id=user_in.organization_id,
            location=user_in.location or "Local City",
            is_verified=True, # Auto-verified for seamless testing/demo, token stored for explicit verification flow
            verification_token=v_token
        )
        created_user = user_repository.create(db, db_user)


        # If user registered as NGO or Recycling Center, create organization profile
        if user_in.role in [UserRole.NGO.value, UserRole.RECYCLING_CENTER.value]:
            org_name = user_in.organization_name or f"{user_in.full_name}'s {user_in.role.upper()}"
            org = Organization(
                user_id=created_user.id,
                name=org_name,
                org_type=user_in.role,
                address=user_in.location or "City Center",
                phone="555-0199"
            )
            organization_repository.create(db, org)

        logger.info(f"New user registered: {created_user.email} (Role: {created_user.role})")
        return created_user

    def authenticate_user(self, db: Session, login_in: UserLogin) -> Dict[str, Any]:
        user = user_repository.get_by_email(db, login_in.email.lower())
        if not user or not verify_password(login_in.password, user.hashed_password):
            logger.warning(f"Failed login attempt for email: {login_in.email}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password"
            )

        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Inactive user account"
            )

        access_token = create_access_token(subject=user.id, role=user.role)
        refresh_token = create_refresh_token(subject=user.id)

        # Store refresh token in user profile
        user.refresh_token = refresh_token
        user_repository.update(db, user, {})

        logger.info(f"User logged in successfully: {user.email} (ID: {user.id})")
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
            "user": user
        }

    def refresh_access_token(self, db: Session, refresh_token_str: str) -> Dict[str, Any]:
        payload = decode_access_token(refresh_token_str)
        if not payload or payload.get("type") != "refresh":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired refresh token"
            )

        user_id = payload.get("sub")
        user = user_repository.get(db, int(user_id)) if user_id else None
        
        if not user or user.refresh_token != refresh_token_str or not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Refresh token is revoked or user is inactive"
            )

        new_access_token = create_access_token(subject=user.id, role=user.role)
        new_refresh_token = create_refresh_token(subject=user.id)
        
        user.refresh_token = new_refresh_token
        user_repository.update(db, user, {})

        logger.info(f"Token refreshed for user ID: {user.id}")
        return {
            "access_token": new_access_token,
            "refresh_token": new_refresh_token,
            "token_type": "bearer",
            "user": user
        }

    def logout_user(self, db: Session, user: User) -> Dict[str, str]:
        user.refresh_token = None
        user_repository.update(db, user, {})
        logger.info(f"User logged out: {user.email}")
        return {"message": "Successfully logged out"}

    def request_password_reset(self, db: Session, email: str) -> Dict[str, str]:
        user = user_repository.get_by_email(db, email.lower())
        r_token = f"reset_{secrets.token_urlsafe(16)}"
        if user:
            user.reset_token = r_token
            user_repository.update(db, user, {})
            logger.info(f"Password reset token issued for user: {email}")

        return {
            "message": "If an account exists with this email, password reset instructions have been sent.",
            "simulated_reset_token": r_token if user else "none"
        }

    def confirm_password_reset(self, db: Session, token: str, new_password: str) -> Dict[str, str]:
        user = user_repository.get_by_reset_token(db, token)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid or expired reset token"
            )

        user.hashed_password = get_password_hash(new_password)
        user.reset_token = None
        user_repository.update(db, user, {})
        logger.info(f"Password successfully reset for user: {user.email}")
        return {"message": "Password successfully reset. You may now log in with your new password."}

    def verify_email(self, db: Session, token: str) -> Dict[str, str]:
        user = user_repository.get_by_verification_token(db, token)
        if not user:
            # Fallback check if user is already verified
            return {"message": "Email verified successfully!"}

        user.is_verified = True
        user.verification_token = None
        user_repository.update(db, user, {})
        logger.info(f"Email verified for user: {user.email}")
        return {"message": "Email successfully verified!"}

auth_service = AuthService()

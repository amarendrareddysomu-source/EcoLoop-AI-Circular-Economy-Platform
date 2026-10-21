from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.deps import get_current_active_user
from app.schemas.user import (
    UserCreate, 
    UserLogin, 
    UserResponse, 
    Token, 
    RefreshTokenInput,
    PasswordReset, 
    PasswordResetConfirm
)
from app.services.auth_service import auth_service
from app.models.user import User

router = APIRouter()

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED, summary="Register a new user account")
def register(user_in: UserCreate, db: Session = Depends(get_db)):
    return auth_service.register_user(db, user_in)

@router.post("/login", response_model=Token, summary="Authenticate user and issue access + refresh tokens")
def login(login_in: UserLogin, db: Session = Depends(get_db)):
    return auth_service.authenticate_user(db, login_in)

@router.post("/login/form", response_model=Token, summary="OAuth2 compatible form login endpoint")
def login_form(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    login_in = UserLogin(email=form_data.username, password=form_data.password)
    return auth_service.authenticate_user(db, login_in)

@router.post("/refresh", response_model=Token, summary="Refresh access token using a valid refresh token")
def refresh_token(token_in: RefreshTokenInput, db: Session = Depends(get_db)):
    return auth_service.refresh_access_token(db, token_in.refresh_token)

@router.post("/logout", summary="Logout current user and invalidate active refresh token")
def logout(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    return auth_service.logout_user(db, current_user)

@router.get("/me", response_model=UserResponse, summary="Get current authenticated user profile")
def get_auth_me(current_user: User = Depends(get_current_active_user)):
    return current_user


@router.post("/password-reset", summary="Request password reset link/token")
def request_password_reset(reset_in: PasswordReset, db: Session = Depends(get_db)):
    return auth_service.request_password_reset(db, reset_in.email)

@router.post("/password-reset/confirm", summary="Confirm password reset with valid reset token")
def confirm_password_reset(confirm_in: PasswordResetConfirm, db: Session = Depends(get_db)):
    return auth_service.confirm_password_reset(db, confirm_in.token, confirm_in.new_password)

@router.get("/verify-email", summary="Verify email address using verification token")
def verify_email(token: str, db: Session = Depends(get_db)):
    return auth_service.verify_email(db, token)

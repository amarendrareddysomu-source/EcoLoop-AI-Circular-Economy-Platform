from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.deps import get_current_active_user, require_admin
from app.schemas.user import UserCreate, UserResponse, UserUpdate
from app.repositories.user_repository import user_repository
from app.services.auth_service import auth_service
from app.models.user import User, UserRole

router = APIRouter()

ALLOWED_USER_MANAGERS = [
    UserRole.SUPER_ADMIN.value,
    UserRole.ORGANIZATION_ADMIN.value,
    UserRole.ADMIN.value
]

ALLOWED_USER_READERS = [
    UserRole.SUPER_ADMIN.value,
    UserRole.ORGANIZATION_ADMIN.value,
    UserRole.STAFF.value,
    UserRole.AUDITOR.value,
    UserRole.ADMIN.value
]

@router.get("/", response_model=List[UserResponse], summary="List all users with optional filtering")
def list_users(
    organization_id: Optional[int] = None,
    role: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    # Enforce role-based scoping: non-super-admin Org Admins can only list users in their own org
    if current_user.role not in [UserRole.SUPER_ADMIN.value, UserRole.ADMIN.value]:
        if current_user.role == UserRole.ORGANIZATION_ADMIN.value:
            organization_id = current_user.organization_id
        elif current_user.role not in ALLOWED_USER_READERS:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to view user directory"
            )

    query = db.query(User)
    if organization_id is not None:
        query = query.filter(User.organization_id == organization_id)
    if role is not None:
        query = query.filter(User.role == role)

    return query.offset(skip).limit(limit).all()

@router.get("/me", response_model=UserResponse, summary="Get current logged-in user profile")
def read_current_user(current_user: User = Depends(get_current_active_user)):
    return current_user

@router.put("/me", response_model=UserResponse, summary="Update current user profile")
def update_current_user_profile(
    user_update: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    update_data = user_update.model_dump(exclude_unset=True)
    # Prevent non-admin from self-elevating role or org via /me
    if current_user.role not in [UserRole.SUPER_ADMIN.value, UserRole.ADMIN.value]:
        if "role" in update_data:
            del update_data["role"]
        if "organization_id" in update_data:
            del update_data["organization_id"]
            
    if "password" in update_data and update_data["password"]:
        from app.core.security import get_password_hash
        update_data["hashed_password"] = get_password_hash(update_data.pop("password"))
        
    return user_repository.update(db, current_user, update_data)

@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED, summary="Create new user (Admin / Org Admin)")
def create_user(
    user_in: UserCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    # Org admins can only create staff/auditors in their own organization
    if current_user.role == UserRole.ORGANIZATION_ADMIN.value:
        if not user_in.organization_id:
            user_in.organization_id = current_user.organization_id
        elif user_in.organization_id != current_user.organization_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Cannot create users outside your assigned organization"
            )

    return auth_service.register_user(db, user_in)

@router.get("/{user_id}", response_model=UserResponse, summary="Get user details by ID")
def get_user_by_id(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    user = user_repository.get(db, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    # Check org admin scoping
    if current_user.role == UserRole.ORGANIZATION_ADMIN.value:
        if user.organization_id != current_user.organization_id and user.id != current_user.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")
            
    return user

@router.put("/{user_id}", response_model=UserResponse, summary="Update user profile or role")
def update_user_by_admin(
    user_id: int,
    user_update: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    target_user = user_repository.get(db, user_id)
    if not target_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    # Authorization checks
    is_super_admin = current_user.role in [UserRole.SUPER_ADMIN.value, UserRole.ADMIN.value]
    is_org_admin = current_user.role == UserRole.ORGANIZATION_ADMIN.value and target_user.organization_id == current_user.organization_id
    is_self = current_user.id == target_user.id

    if not (is_super_admin or is_org_admin or is_self):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to edit this user")

    update_data = user_update.model_dump(exclude_unset=True)
    if not is_super_admin:
        if "role" in update_data and update_data["role"] != target_user.role:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only Super Admin can change user roles")

    if "password" in update_data and update_data["password"]:
        from app.core.security import get_password_hash
        update_data["hashed_password"] = get_password_hash(update_data.pop("password"))

    return user_repository.update(db, target_user, update_data)

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete user account")
def delete_user_by_admin(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    target_user = user_repository.get(db, user_id)
    if not target_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    if current_user.role == UserRole.ORGANIZATION_ADMIN.value:
        if target_user.organization_id != current_user.organization_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Cannot delete users from other organizations")

    user_repository.delete(db, user_id)
    return None

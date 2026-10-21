from typing import List, Optional
from fastapi import APIRouter, Depends, UploadFile, File, Form, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.deps import get_current_active_user
from app.schemas.item import ItemCreate, ItemResponse, ItemUpdate
from app.services.item_service import item_service
from app.services.upload_service import upload_service
from app.models.user import User, UserRole

router = APIRouter()

@router.post("/", response_model=ItemResponse, status_code=status.HTTP_201_CREATED, summary="Create a new item via JSON payload")
def create_item_json(
    item_in: ItemCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    return item_service.create_item(db, current_user.id, item_in)

@router.post("/upload", response_model=ItemResponse, status_code=status.HTTP_201_CREATED, summary="Upload item with secure image validation")
async def upload_item_with_image(
    title: str = Form(...),
    category: str = Form(...),
    description: Optional[str] = Form(""),
    brand: Optional[str] = Form("Generic"),
    age_years: float = Form(1.0),
    usage_level: Optional[str] = Form("Moderate"),
    condition: str = Form("Good"),
    original_price: float = Form(100.0),
    location: Optional[str] = Form("Local City"),
    image: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    image_bytes = None
    image_url = None
    if image and image.filename:
        image_bytes = await image.read()
        image_url, _ = upload_service.save_image(image, image_bytes)

    item_in = ItemCreate(
        title=title,
        description=description,
        category=category,
        brand=brand,
        age_years=age_years,
        usage_level=usage_level,
        condition=condition,
        original_price=original_price,
        location=location,
        image_url=image_url
    )
    return item_service.create_item(db, current_user.id, item_in, image_bytes=image_bytes)

@router.get("/", response_model=List[ItemResponse], summary="List public items with optional filters")
def list_items(
    category: Optional[str] = None,
    status_filter: Optional[str] = None,
    db: Session = Depends(get_db)
):
    return item_service.get_all_items(db, category=category, status_filter=status_filter)

@router.get("/my-items", response_model=List[ItemResponse], summary="List items created by current logged-in user")
def get_user_items(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    return item_service.get_user_items(db, current_user.id)

@router.get("/{item_id}", response_model=ItemResponse, summary="Get item details by ID")
def get_item_by_id(item_id: int, db: Session = Depends(get_db)):
    return item_service.get_item(db, item_id)

@router.put("/{item_id}", response_model=ItemResponse, summary="Update existing item details")
def update_item(
    item_id: int,
    item_update: ItemUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    is_admin = current_user.role == UserRole.ADMIN.value
    return item_service.update_item(db, item_id, current_user.id, item_update, is_admin=is_admin)

@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete item by ID")
def delete_item(
    item_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    is_admin = current_user.role == UserRole.ADMIN.value
    item_service.delete_item(db, item_id, current_user.id, is_admin=is_admin)
    return None

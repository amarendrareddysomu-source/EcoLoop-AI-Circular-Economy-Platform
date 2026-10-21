from fastapi import APIRouter, Depends, UploadFile, File, Form, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.ai import (
    ImageAnalysisRequest,
    AIAnalysisResult,
    AISustainabilityRequest,
    AISustainabilityResponse,
    PricePredictionRequest,
    PricePredictionResponse,
    ConditionPredictionRequest,
    ConditionPredictionResponse,
    RecommendationRequest,
    RecommendationResponse,
    ImageClassificationResponse,
    HybridVisionIdentifyResponse,
    HybridAnalysisRequest,
    HybridAnalysisResponse,
    ManualClassificationRequest,
    ManualClassificationResponse
)
from app.services.ai_service import ai_service
from app.services.upload_service import upload_service

router = APIRouter()

@router.post(
    "/classify-image",
    response_model=ImageClassificationResponse,
    status_code=status.HTTP_200_OK,
    summary="Classify uploaded item image and run end-to-end AI prediction pipeline",
    description="Accepts image file (JPG, JPEG, PNG, WEBP <= 10MB), validates, preprocesses, and predicts object category, condition, repairability score, sustainability score, price, and circular recommendations."
)
async def classify_image(
    image: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    image_bytes = await image.read()
    return ai_service.classify_image_pipeline(db=db, file=image, file_bytes=image_bytes)


@router.post(
    "/manual-classify",
    response_model=ManualClassificationResponse,
    status_code=status.HTTP_200_OK,
    summary="Manually evaluate item details through full AI decision pipeline",
    description="Accepts manual item inputs (Item Name, Category, Condition, Weight, Age, Price) and executes full circular economy AI decision engine."
)
def manual_classify(
    req: ManualClassificationRequest,
    db: Session = Depends(get_db)
):
    return ai_service.manual_classify_pipeline(db=db, req=req)



# --- New Phase 7 Advanced AI Inference Endpoints ---

@router.post(
    "/predict-price",
    response_model=PricePredictionResponse,
    summary="Predict item resale price based on ML model & market factors"
)
def predict_price(req: PricePredictionRequest, db: Session = Depends(get_db)):
    return ai_service.predict_price(db, req)

@router.post(
    "/predict-condition",
    response_model=ConditionPredictionResponse,
    summary="Classify item condition using age, usage level, and metadata"
)
def predict_condition(req: ConditionPredictionRequest, db: Session = Depends(get_db)):
    return ai_service.predict_condition(db, req)

@router.post(
    "/sustainability-score",
    response_model=AISustainabilityResponse,
    summary="Calculate item sustainability score (0-100) and environmental impact category"
)
def calculate_sustainability_score(req: AISustainabilityRequest, db: Session = Depends(get_db)):
    return ai_service.predict_sustainability_score(db, req)

@router.post(
    "/recommend",
    response_model=RecommendationResponse,
    summary="Generate circular recommendations for reuse, recycling, and NGO routing"
)
def recommend_circular_actions(req: RecommendationRequest, db: Session = Depends(get_db)):
    return ai_service.recommend(db, req)

# --- Legacy Multimodal AI Endpoints ---

@router.post("/analyze", response_model=AIAnalysisResult, summary="Analyze item metadata via AI pipeline")
def analyze_item_metadata(req: ImageAnalysisRequest, db: Session = Depends(get_db)):
    res = ai_service.analyze_item(
        db=db,
        category_hint=req.category,
        age_years=req.age_years,
        usage_level=req.usage_level,
        original_price=req.original_price
    )
    return res

@router.post("/analyze-image", response_model=AIAnalysisResult, summary="Analyze uploaded image and item metadata")
async def analyze_uploaded_image(
    category_hint: str = Form(None),
    brand: str = Form("Generic"),
    age_years: float = Form(1.0),
    usage_level: str = Form("Moderate"),
    original_price: float = Form(100.0),
    condition: str = Form(None),
    image: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    image_bytes = await image.read()
    res = ai_service.analyze_item(
        db=db,
        image_bytes=image_bytes,
        category_hint=category_hint,
        brand=brand,
        age_years=age_years,
        usage_level=usage_level,
        original_price=original_price,
        user_stated_condition=condition
    )
    return res

# --- Major Hybrid AI System Endpoints (CV + User Metadata) ---

@router.post(
    "/vision-identify",
    response_model=HybridVisionIdentifyResponse,
    summary="Phase 1: Computer Vision Object & Material Identification ONLY"
)
async def vision_identify(
    image: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    image_bytes = await image.read()
    upload_service.validate_image(image, image_bytes)
    return ai_service.analyze_vision_identify(image_bytes)

@router.post(
    "/hybrid-predict",
    response_model=HybridAnalysisResponse,
    summary="Phases 3-8: Hybrid AI Fusion Engine combining Vision + 25 User Metadata fields"
)
async def hybrid_predict(
    req: HybridAnalysisRequest,
    db: Session = Depends(get_db)
):
    metadata_dict = req.model_dump()
    return ai_service.analyze_hybrid_pipeline(image_bytes=None, metadata_dict=metadata_dict)

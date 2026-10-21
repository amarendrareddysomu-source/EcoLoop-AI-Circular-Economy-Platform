from sqlalchemy import Column, Integer, String, Float, Text, DateTime
from sqlalchemy.sql import func
from app.core.database import Base

class AILog(Base):
    __tablename__ = "ai_logs"

    id = Column(Integer, primary_key=True, index=True)
    item_id = Column(Integer, nullable=True, index=True)
    module_name = Column(String, nullable=False, index=True) # ImageClassifier, PricePredictor, etc.
    model_version = Column(String, nullable=False, default="1.0.0")
    execution_time_ms = Column(Float, nullable=False)
    input_summary = Column(Text, nullable=True)
    output_summary = Column(Text, nullable=True)
    confidence_score = Column(Float, nullable=True)
    status = Column(String, nullable=False, default="SUCCESS", index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)


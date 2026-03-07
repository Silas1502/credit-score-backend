from sqlalchemy import Column, String, Boolean, Float, DateTime
from sqlalchemy.dialects.postgresql import UUID, JSONB
from datetime import datetime
import uuid
from .database import Base


class Application(Base):
    __tablename__ = "applications"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    input_data = Column(JSONB)
    approval_score = Column(Float)
    approved = Column(Boolean)
    risk_level = Column(String)
    recommendation = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
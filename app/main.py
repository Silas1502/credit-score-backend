from typing import List
from sqlalchemy import func, text
from fastapi import HTTPException
from app.model_loader import model
from sqlalchemy.orm import Session
from app.schemas import CreditInput
from fastapi import FastAPI, Depends
from app.model_loader import predict
from app.database import get_db, engine
from app.models import Application, Base
from app.schemas import ApplicationResponse
from fastapi.middleware.cors import CORSMiddleware

try:
    Base.metadata.create_all(bind=engine)
except Exception as e:
    print("Database connection failed:", e)

app = FastAPI()

origins = [
    "http://localhost:3000",   # React frontend
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "API working"}

@app.get("/health")
def health(db: Session = Depends(get_db)):

    try:
        db.execute(text("SELECT 1"))
        db_status = "connected"
    except:
        db_status = "disconnected"

    return {
        "status": "ok",
        "model_loaded": True,
        "database": db_status
    }

@app.post("/predict")
def predict_credit(data: CreditInput, db: Session = Depends(get_db)):

    print("INPUT:", data.model_dump())

    result = predict(data.model_dump())

    print("RESULT:", result)

    try:
        record = Application(
            input_data=data.model_dump(),
            approval_score=result["approval_score"],
            approved=result["approved"],
            risk_level=result["risk_level"],
            recommendation=result["recommendation"]
        )

        db.add(record)
        db.commit()
        db.refresh(record)

    except Exception as e:
        print("Database error:", e)

    return result

@app.get("/applications")
def get_applications(
    page: int = 1, 
    page_size: int = 10, 
    db: Session = Depends(get_db)):

    offset = (page - 1) * page_size

    items = (
        db.query(Application)
        .order_by(Application.created_at.desc()) 
        .offset(offset)
        .limit(page_size)
        .all()
    )

    total = db.query(Application).count()

    approved = db.query(Application).filter(
    Application.approved == True
    ).count()

    avg_score = db.query(func.avg(Application.approval_score)).scalar()

    return {
        "items": items,
        "total": total,
        "approved": approved,
        "avg_score": avg_score
    }

@app.get("/applications/{id}")
def get_application(id: str, db: Session = Depends(get_db)):
    
    application = db.query(Application).filter(Application.id == id).first()

    if application is None:
        raise HTTPException(status_code=404, detail="Application not found")

    return application

@app.get("/model-info")
def model_info():
    return {
        "model_name": "Credit Approval Model",
        "model_type": type(model).__name__,
        "version": "1.0",
        "features": list(model.feature_names_in_),
        "target": "approved"
    }
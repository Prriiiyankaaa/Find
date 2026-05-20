"""
Feedback router - API endpoints for user corrections/feedback
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Optional, Dict
from datetime import datetime

from find_api.core.database import get_db
from find_api.models.feedback import Feedback
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

# ─── Pydantic schemas ──────────────────────────────────────────────────────────


class FeedbackCreate(BaseModel):
    """Payload to create new feedback"""

    feedback_type: str  # 'same_person' or 'image_assignment'
    source_id: int
    target_id: Optional[int] = None
    media_id: Optional[int] = None
    decision: str  # 'confirm' or 'reject'
    metadata_json: Optional[Dict] = None


class FeedbackResponse(BaseModel):
    """Feedback item response"""

    id: int
    feedback_type: str
    source_id: int
    target_id: Optional[int]
    media_id: Optional[int]
    decision: str
    metadata_json: Optional[Dict]
    created_at: datetime
    is_active: bool

    class Config:
        from_attributes = True


# ─── Endpoints ────────────────────────────────────────────────────────────────


@router.post("/feedback", response_model=FeedbackResponse)
def create_feedback(data: FeedbackCreate, db: Session = Depends(get_db)):
    """
    Store user feedback/correction for a grouping.
    """
    # Create feedback entry
    feedback = Feedback(
        feedback_type=data.feedback_type,
        source_id=data.source_id,
        target_id=data.target_id,
        media_id=data.media_id,
        decision=data.decision,
        metadata_json=data.metadata_json,
        is_active=True,
    )

    db.add(feedback)
    db.commit()
    db.refresh(feedback)

    logger.info(f"Created feedback {feedback.id} type={feedback.feedback_type}")
    return feedback


@router.get("/feedback", response_model=List[FeedbackResponse])
def list_feedback(
    feedback_type: Optional[str] = None,
    source_id: Optional[int] = None,
    media_id: Optional[int] = None,
    is_active: Optional[bool] = True,
    db: Session = Depends(get_db),
):
    """
    List historical feedback items.
    """
    query = db.query(Feedback)

    if feedback_type:
        query = query.filter(Feedback.feedback_type == feedback_type)
    if source_id:
        query = query.filter(Feedback.source_id == source_id)
    if media_id:
        query = query.filter(Feedback.media_id == media_id)
    if is_active is not None:
        query = query.filter(Feedback.is_active == is_active)

    return query.order_by(Feedback.created_at.desc()).all()


@router.post("/feedback/{feedback_id}/revert", response_model=FeedbackResponse)
def revert_feedback(feedback_id: int, db: Session = Depends(get_db)):
    """
    Mark feedback as inactive (revert the correction).
    """
    feedback = db.query(Feedback).filter(Feedback.id == feedback_id).first()
    if not feedback:
        raise HTTPException(status_code=404, detail="Feedback not found")

    feedback.is_active = False
    db.commit()
    db.refresh(feedback)

    logger.info(f"Reverted feedback {feedback_id}")
    return feedback


@router.delete("/feedback/{feedback_id}")
def delete_feedback(feedback_id: int, db: Session = Depends(get_db)):
    """
    Permanently delete a feedback item.
    """
    feedback = db.query(Feedback).filter(Feedback.id == feedback_id).first()
    if not feedback:
        raise HTTPException(status_code=404, detail="Feedback not found")

    db.delete(feedback)
    db.commit()

    return {"status": "deleted", "id": feedback_id}

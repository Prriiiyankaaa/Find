"""
User feedback model for correcting ML groupings (e.g. People)
"""

from sqlalchemy import Column, Integer, String, DateTime, Boolean, JSON, ForeignKey
from sqlalchemy.sql import func
from find_api.core.database import Base


class Feedback(Base):
    """
    Stores local user corrections for ML groupings.
    This data can be used to improve clustering in future runs.
    """

    __tablename__ = "feedback"

    id = Column(Integer, primary_key=True, index=True)

    # Type of feedback: 'same_person' or 'image_assignment'
    feedback_type = Column(String(50), nullable=False)

    # Source person_id or cluster_id
    source_id = Column(Integer, nullable=False, index=True)

    # Target person_id or cluster_id (used for 'same_person' feedback)
    target_id = Column(Integer, nullable=True, index=True)

    # Media ID (used for 'image_assignment' feedback)
    media_id = Column(
        Integer,
        ForeignKey("media.id", ondelete="CASCADE"),
        nullable=True,
        index=True,
    )

    # Decision: 'confirm' (belong together) or 'reject' (don't belong together)
    decision = Column(String(20), nullable=False)

    # Optional metadata (e.g. labels, reason)
    metadata_json = Column(JSON, nullable=True)

    # When the feedback was given
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Whether this feedback is currently applied (active) or has been reverted
    is_active = Column(Boolean, nullable=False, default=True)

    def __repr__(self):
        return (
            f"<Feedback(id={self.id}, "
            f"type={self.feedback_type}, "
            f"decision={self.decision}, "
            f"active={self.is_active})>"
        )

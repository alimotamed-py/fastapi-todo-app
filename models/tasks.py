#==================== Add Library And Package ====================
from sqlalchemy import Column, String, Text, func, Boolean, Integer, DateTime, ForeignKey
from app.database import Base
from sqlalchemy.orm import relationship


#==================== Task Model ====================
class TaskModel(Base):
    __tablename__ = "Task"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    title = Column(String(150), nullable=False)
    description = Column(Text(500), nullable=True)
    is_completed = Column(Boolean, default=False)
    
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), server_onupdate=func.now())
    
    # Relationship
    user = relationship("UserModel", back_populates="tasks", uselist=False)
    
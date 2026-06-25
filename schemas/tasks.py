#==================== Add Library And Package ====================
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime



class TaskSchema(BaseModel):
    title: str = Field(..., min_length=5, max_length=150, description="Title of the Task")
    description: Optional[str] = Field(None, max_length=500, description="Description of the Task")
    is_completed: bool = Field(..., description="State of the Task")
    

class TaskCreateSchema(BaseModel):
    pass

class TaskUpdateSchema(BaseModel):
    pass

class TaskResponseSchema(BaseModel):
    id: int = Field(..., description="Unique identifier of the object.")
    
    created_at: datetime = Field(..., description="Creation date and time of the object")
    updated_at: datetime = Field(..., description="Updating date and time of the object")



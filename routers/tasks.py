#==================== Add Library And Package ====================
from fastapi import APIRouter, Path, Depends, HTTPException, status, Query
from schemas.tasks import TaskResponseSchema, TaskCreateSchema, TaskUpdateSchema
from models.tasks import TaskModel
from models.users import UserModel
from sqlalchemy.orm import Session
from app.database import get_db
from typing import List
from auth.jwt_auth import get_authenticated_user


#==================== Routers ====================
router = APIRouter()


#==================== Retrieve Task List ====================
@router.get("/task", response_model=List[TaskResponseSchema],)
async def task_list(
    completed: bool = Query(None, description="filter tasks based on being completed or not!!"),
    limit: int = Query(10, gt=0, le=50, description="limiting the number of item to retrieve!!"),
    offset: int = Query(0, ge=0, description="use for paginating base on passed item!!"),
    db: Session = Depends(get_db),
    user: UserModel = Depends(get_authenticated_user)):
    
    query = db.query(TaskModel).filter_by(user_id=user.id)
    if completed is not None:
        query = query.filter_by(is_completed=completed)
        
    return query.limit(limit).offset(offset).all()


#==================== Retrieve Task Detail ====================
@router.get("/task/{task_id}", response_model=TaskResponseSchema)
async def task_detail(task_id: int = Path(..., gt=0), db: Session = Depends(get_db),
                      user: UserModel = Depends(get_authenticated_user)):
    task_object = db.query(TaskModel).filter_by(user_id=user.id, id=task_id).first()
    if not task_object:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found!!")
    return task_object


#==================== Create Task ====================
@router.post("/task", response_model=TaskResponseSchema)
async def create_task(request: TaskCreateSchema, db: Session = Depends(get_db),
                      user: UserModel = Depends(get_authenticated_user)):
    data = request.model_dump()
    data.update({"user_id" : user.id})
    task_object = TaskModel(**data)
    db.add(task_object)
    db.commit()
    db.refresh(task_object)
    return task_object


#==================== Update Task ====================
@router.put("/task/{task_id}", response_model=TaskResponseSchema)
async def update_task(request: TaskUpdateSchema, task_id: int = Path(..., gt=0), db: Session = Depends(get_db),
                      user: UserModel = Depends(get_authenticated_user)):
    task_object = db.query(TaskModel).filter_by(user_id=user.id, id=task_id).first()
    if not task_object:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found!!")
    
    for field, value in request.model_dump(exclude_unset=True).items():
        setattr(task_object, field, value)
        
    db.commit()
    db.refresh(task_object)
    return task_object


#==================== Delete Task ====================
@router.delete("/task/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(task_id: int = Path(..., gt=0), db: Session = Depends(get_db),
                      user: UserModel = Depends(get_authenticated_user)):
    task_object = db.query(TaskModel).filter_by(user_id=user.id, id=task_id).first()
    if not task_object:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found!!")
    
    db.delete(task_object)
    db.commit()
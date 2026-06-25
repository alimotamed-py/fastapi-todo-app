# ==================== Add Library And Package ====================
from fastapi import APIRouter, Path, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from schemas.users import UserLoginSchema, UserRegisterSchema, UserRefresdhTokenSchema
from models.users import UserModel
from sqlalchemy.orm import Session
from app.database import get_db
from auth.jwt_auth import generate_access_token, generate_refresh_token, decode_refresh_token


# ==================== Instance ====================
router = APIRouter()

# ====================  User Login ====================


@router.post("/login")
async def user_login(request: UserLoginSchema, db: Session = Depends(get_db)):
    user_object = db.query(UserModel).filter_by(
        username=request.username.lower()).first()
    if not user_object:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="username or password is wrong..!")
    if not user_object.verify_password(request.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="username or password is wrong..!")

    access_token = generate_access_token(user_object.id)
    refresh_token = generate_refresh_token(user_object.id)
    return JSONResponse(content={
        "Detail": "Logged in Successfully",
        "Access Token": access_token,
        "Refresh Token": refresh_token
    })


# ==================== User Register ====================
@router.post("/register")
async def user_register(request: UserRegisterSchema, db: Session = Depends(get_db)):
    if db.query(UserModel).filter_by(username=request.username.lower()).first():
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="username already exists!!")
    user_object = UserModel(username=request.username.lower())
    user_object.set_password(request.password)
    db.add(user_object)
    db.commit()
    return JSONResponse(status_code=status.HTTP_201_CREATED, content={"detail": "User registerd Successfully!!"})


# ==================== User Register ====================
@router.post("/redresh-token")
async def user_refresh_token(request: UserRefresdhTokenSchema, db: Session = Depends(get_db)):
    user_id = decode_refresh_token(request.token)
    access_toekn = generate_access_token(user_id)
    return JSONResponse(content={"access token": access_toekn})

#==================== Add Library And Package ====================
from pydantic import BaseModel, Field, field_validator
from fastapi import HTTPException, status

#==================== User Login Schema ====================
class UserLoginSchema(BaseModel):
    username: str = Field(..., max_length=150, description="username of the user")
    password: str = Field(..., description="password of the user")
    
    
    #==================== User Register Schema ====================
class UserRegisterSchema(BaseModel):
    username: str = Field(..., max_length=150, description="username of the user")
    password: str = Field(..., description="password of the user")
    password_confrim: str = Field(..., description="confrim password of the user")
    
    
    @field_validator("password_confrim")
    def check_password_match(cls, password_confrim, validation):
        if not password_confrim == validation.data.get("password"):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="password dosent match!!")
        return password_confrim
    
    
    
class UserRefresdhTokenSchema(BaseModel):
    token: str = Field(..., description="redresh token of the user")
    
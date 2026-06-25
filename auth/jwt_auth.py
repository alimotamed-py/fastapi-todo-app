#==================== Add Library And Package ====================
import jwt
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi import Depends, HTTPException, status
from app.database import get_db
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from app.settings import Settings
from jwt.exceptions import DecodeError, InvalidSignatureError
from models.users import UserModel


security = HTTPBearer()


#==================== Authenticated User ====================
def get_authenticated_user(credentials: HTTPAuthorizationCredentials, db: Session = Depends(security)):
    token = credentials.credentials
    try:
        decoded = jwt.decode(token, Settings.JWT_SECRET_KEY, algorithm= Settings.JWT_ALGORITHM)
        user_id = decoded.get("user_id", None)
        if not user_id:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail="Authenticatin failed!! user_id not in the payload")
        
        if decoded.get("type") != "access":
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                 detail="Authenticatin failed!! Token is not Valid")
            
        if datetime.now() > datetime.fromtimestamp(decoded.get("exp")):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                 detail="Authenticatin failed!! Token Expired")
        
        user_object = db.query(UserModel).filter_by(id=user_id).one()
        return user_object
                 
        
    except InvalidSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Authenticatin failed!! Invalid Signature")
        
    except DecodeError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Authenticatin failed!! Decode Error")
        
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail=f"Authenticatin failed!! {e}")
    
        


#==================== Access Token ====================
def generate_access_token(user_id: int, expires_in: int = 60*5) -> str:
    now = datetime.utcnow()
    payload = {
        "type" : "access",
        "user_id" : user_id,
        "iat" : now,
        "exp" : now + timedelta(seconds= expires_in)
    }
    return jwt.encode(payload, Settings.JWT_SECRET_KEY, algorithm= Settings.JWT_ALGORITHM)


#==================== Refresh Token ====================
def generate_refresh_token(user_id: int, expires_in: int = 3600*24) -> str:
    now = datetime.utcnow()
    payload = {
        "type" : "refresh",
        "user_id" : user_id,
        "iat" : now,
        "exp" : now + timedelta(seconds= expires_in)
    }
    return jwt.encode(payload, Settings.JWT_SECRET_KEY, algorithm= Settings.JWT_ALGORITHM)



def decode_refresh_token(token):
    try:
        decoded = jwt.decode(token, Settings.JWT_SECRET_KEY, algorithm= Settings.JWT_ALGORITHM)
        user_id = decoded.get("user_id", None)
        if not user_id:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail="Authenticatin failed!! user_id not in the payload")
        
        if decoded.get("type") != "refresh":
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                 detail="Authenticatin failed!! Token is not Valid")
            
        if datetime.now() > datetime.fromtimestamp(decoded.get("exp")):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                 detail="Authenticatin failed!! Token Expired")
        
        return user_id
                 
        
    except InvalidSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Authenticatin failed!! Invalid Signature")
        
    except DecodeError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Authenticatin failed!! Decode Error")
        
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail=f"Authenticatin failed!! {e}")
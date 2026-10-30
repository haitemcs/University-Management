import jwt
from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session, joinedload
from app.database import get_db
from app.models import User
from app.security import decode_access_token

bearer_scheme = HTTPBearer(auto_error=False)

def get_current_user(credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme), db: Session = Depends(get_db)) -> User:
    unauthorized = HTTPException(status_code=401, detail="Invalid or expired token", headers={"WWW-Authenticate": "Bearer"})
    if credentials is None:
        raise unauthorized
    try:
        user_id = int(decode_access_token(credentials.credentials).get("sub", ""))
    except (jwt.InvalidTokenError, ValueError, TypeError):
        raise unauthorized
    user = db.query(User).options(joinedload(User.role)).filter(User.id == user_id, User.is_active.is_(True)).first()
    if not user:
        raise unauthorized
    return user

def require_roles(*roles: str):
    def checker(user: User = Depends(get_current_user)) -> User:
        if user.role.name not in roles:
            raise HTTPException(status_code=403, detail="Insufficient permissions")
        return user
    return checker

from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext 
import os
from dotenv import load_dotenv
from sqlalchemy.orm import Session  # Ajout

from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status

from app.database import get_db  # Vous devez créer cette fonction
from app import models  # Pour accéder au modèle User

# Charger les variables d'environnement
load_dotenv()

# Configuration
SECRET_KEY = os.getenv("SECRET_KEY", "your_default_secret_key_but_change_in_production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

## validation
import warnings

# Validation de la secret key
if "SECRET_KEY" not in os.environ:
    warnings.warn(
        "SECRET_KEY non définie dans les variables d'environnement, "
        "utilisation de la valeur par défaut (INSÉCURE pour la production)",
        UserWarning,
        stacklevel=2
    )
elif SECRET_KEY == "your_default_secret_key_but_change_in_production":
    warnings.warn(
        "Vous utilisez la secret key par défaut (INSÉCURE pour la production) !",
        UserWarning,
        stacklevel=2
    )


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Créer un token JWT"""
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta  # Utilisez utcnow() pour éviter les problèmes de timezone
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")  # Changé pour correspondre à notre route

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)  # Besoin de la session DB
):
    """Décode et vérifie le token JWT, retourne l'utilisateur"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    # Récupérer l'utilisateur depuis la base de données
    user = db.query(models.User).filter(models.User.username == username).first()
    if user is None:
        raise credentials_exception
    return user

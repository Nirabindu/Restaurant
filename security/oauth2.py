from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from security import tokens
from sql_app import models,database,schemas
from sqlalchemy.orm import Session


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def get_current_user(token: str = Depends(oauth2_scheme),db:Session = Depends(database.get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials", headers={"WWW-Authenticate": "Bearer"},)
    return tokens.verify_token(token, credentials_exception,db)
    
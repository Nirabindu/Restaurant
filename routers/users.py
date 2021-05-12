from fastapi import APIRouter, HTTPException, Depends, status,File,UploadFile
from sql_app import schemas,models,database
from sqlalchemy.orm import Session
import shortuuid
from security import hashing,tokens,oauth2
from typing import List







#user registration
router = APIRouter(tags=['users'])
@router.post('/reg/')
async def user_registration(request:schemas.Users,db:Session = Depends(database.get_db)): 

    check_email = db.query(models.Users).filter(models.Users.email == request.email).first()
    check_mobile = db.query(models.Users).filter(models.Users.mobile_no == request.mobile_no).first()
    if check_email:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,detail=f'Email id already register enter anouther email id')
    elif check_mobile:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,detail=f'mobile no already register please use anouther mobile no')

    new_user = models.Users(
        user_id = shortuuid.uuid(),
        name = request.name, 
        email = request.email, 
        password = hashing.Hash.bcrypt(request.password),
        mobile_no = request.mobile_no,
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return{'Account Successfully created please login'}


@router.post('/login/')
def user_login(request:oauth2.OAuth2PasswordRequestForm = Depends() ,db:Session  = Depends(database.get_db)):
    user_email_check = db.query(models.Users).filter(models.Users.email == request.username).first()
    if not user_email_check:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Invalid Email id')
    if not hashing.Hash.verify(user_email_check.password,request.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Invalid password')

    access_token = tokens.create_access_token(data={"sub":  user_email_check.email})
    return {"access_token": access_token, "token_type": "bearer"}
    



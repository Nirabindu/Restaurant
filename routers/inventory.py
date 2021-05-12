from fastapi import APIRouter,HTTPException,Depends
from sql_app import database,schemas,models
from security import hashing, oauth2, tokens
from sqlalchemy.orm import Session











router = APIRouter(tags=['Inventory'])


#adding Ingredients

@router.post('/adding_ingredients/')
def adding_ingredients(ingredients_name:str,units:float,db:Session = Depends(database.get_db),current_user : schemas.Users = Depends(oauth2.get_current_user)):
    


    new_ing_item = models.Ingredients(
        ingredient_name = ingredients_name,
        ing_quantity = units
    )
    db.add(new_ing_item)
    db.commit()
    db.refresh(new_ing_item)
    return {'ingredients added'}


#adding Recipe

# @router.post('/Recipe/')
# def adding_recipe(item_id:int,db:Session = Depends(database.get_db),current_user : schemas.Users = Depends(oauth2.get_current_user)):
#     pass

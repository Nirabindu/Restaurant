from fastapi import APIRouter,HTTPException,Depends
from sqlalchemy.sql.functions import mode
from sql_app import database,schemas,models
from security import hashing, oauth2, tokens
from sqlalchemy.orm import Session
from typing import List











router = APIRouter(tags=['Inventory'])


#adding Ingredients

@router.post('/adding_ingredients/')
def adding_ingredients(ingredient_name:str,units:float,db:Session = Depends(database.get_db),current_user : schemas.Users = Depends(oauth2.get_current_user)):
    
    checking_ingredient = db.query(models.Ingredients).filter(models.Ingredients.ingredient_name == ingredient_name).first()
    
    if checking_ingredient:
        checking_ingredient.ing_quantity = checking_ingredient.ing_quantity + (units * 1000)
        db.commit()
        return{'added'}

    else:
        new_ing_item = models.Ingredients(
            ingredient_name = ingredient_name,
            ing_quantity = units*1000
        )
        db.add(new_ing_item)
        db.commit()
        db.refresh(new_ing_item)
        return {'ingredients added'}

   
#adding Recipe

@router.post('/Recipe/')
def adding_recipe(item_id:int,ing_id:int,ingredients_quantity:float, db:Session = Depends(database.get_db),current_user : schemas.Users = Depends(oauth2.get_current_user)):
    get_item = db.query(models.Items).filter(models.Items.item_id == item_id).first()
    if not get_item:
        return{"Item not matched"}
    
    recipe_item = db.query(models.Recipe).filter(models.Recipe.item_id == item_id).first()
    if not recipe_item:
        add_recipe = models.Recipe(
            item_id = get_item.item_id,
            item_name = get_item.item_name
        )
        db.add(add_recipe)
        db.commit()
        db.refresh(add_recipe)

    get_recipe_id = db.query(models.Recipe).filter(models.Recipe.item_id == item_id).first()

    get_ingredient = db.query(models.Ingredients).filter(models.Ingredients.ing_id == ing_id).first()

    if not get_ingredient:
        return{'Ingredient not found'}

    # checking_ingredient_into_recipe = db.query(models.IngredientsForRecipe).filter(models.IngredientsForRecipe.ing_id == ing_id).where(models.IngredientsForRecipe.recipe_id == models.Recipe.recipe_id).first()

    # if checking_ingredient_into_recipe:
    #     return{'Ingredient already added'}
    # else:
    adding_ingredients_to_recipe = models.IngredientsForRecipe(
        ing_id = get_ingredient.ing_id,
        ingredient_name = get_ingredient.ingredient_name,
        ingredients_quantity = ingredients_quantity,
        recipe_id = get_recipe_id.recipe_id,
        ) 

    db.add(adding_ingredients_to_recipe)
    db.commit()
    db.refresh(adding_ingredients_to_recipe)
    return{'Added'}

#Show Recipe        

@router.get('/show_recipes/',response_model =List[schemas.show_recipe])
def show_recipe(db:Session = Depends(database.get_db),current_user : schemas.Users = Depends(oauth2.get_current_user)):

    show_recipe = db.query(models.Recipe).all()
    return show_recipe

#Edit recipe 

@router.put('/edit_ingredients_for_recipe/')
def edit_ingredients_recipe(ingredientsForRecipe_id:int,ingredients_quantity:float,db:Session = Depends(database.get_db),current_user : schemas.Users = Depends(oauth2.get_current_user)):

    getting_ingredients_for_recipe = db.query(models.IngredientsForRecipe).filter(models.IngredientsForRecipe.ingredientsForRecipe_id == ingredientsForRecipe_id).first()
    if not getting_ingredients_for_recipe:
        return{'invalid'}
    
    getting_ingredients_for_recipe.ingredients_quantity = ingredients_quantity
    db.commit()
    db.refresh(getting_ingredients_for_recipe)
    return {'update'}

#adding item to available table

@router.post('/adding_made_items')
def adding_to_made_item(item_id:int,quantity:int,db:Session = Depends(database.get_db),current_user : schemas.Users = Depends(oauth2.get_current_user)):
    checking_made_item = db.query(models.Made_item).filter(models.Made_item.item_id == item_id).first()

    getting_item = db.query(models.Items).filter(models.Items.item_id == item_id).first()

    if  checking_made_item:
        return{"Item already available"}

    new_made_item = models.Made_item(
        item_id = getting_item.item_id,
        item_name = getting_item.item_name,
        quantity = quantity,
        avalability = quantity,

    )

    # getting recipe for made item

    getting_recipe = db.query(models.Recipe).filter(models.Recipe.item_id == item_id).first()

    if not getting_recipe:
        return{'recipe for the item not found'}

    else:
        getting_ingredient_recipe = db.query(models.IngredientsForRecipe).filter(getting_recipe.recipe_id == models.IngredientsForRecipe.recipe_id).all()
        
        for i in range(quantity):
            for j in getting_ingredient_recipe:
                ing = db.query(models.Ingredients).filter(models.Ingredients.ing_id == j.ing_id).first()
                ing.ing_quantity = ing.ing_quantity - j.ingredients_quantity
                db.commit()

    db.add(new_made_item)
    db.commit()
    db.refresh(new_made_item)
    return{'Added'}



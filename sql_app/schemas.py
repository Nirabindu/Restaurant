from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class Users(BaseModel):
    name: str
    mobile_no: int
    email: str
    password: str


class User_login(BaseModel):
    email: str
    password: str


class Category(BaseModel):
    category_id: int
    category_name: str
    discount: float
    status: bool
    img: str
    create_at: datetime
    class Config():
        orm_mode = True


class SubCategory(BaseModel):
    sub_category_id: int
    sub_category_name: str
    status: bool
    create_at: datetime
    img: str
    class Config():
        orm_mode = True

class Items(BaseModel):
    item_name: str
    item_price: float
    MRP: float
    discount: float
    item_description: str
    item_features: str
    status: bool
    avalability: bool
    tax: float
    create_at: datetime
    class Config():
        orm_mode = True


class Item_img(BaseModel):
    item_img: str
    class Config():
        orm_mode = True


class Breakfast(BaseModel):
    breakfast_id: int
    class Config():
        orm_mode = True
class Lunch(BaseModel):
    lunch_id: int
    class Config():
        orm_mode = True



class Dinner(BaseModel):
    dinner_id: int




# showing data

class Show_category(Category):
    pass


class Show_category_sub_category(Category):
    sub: List[SubCategory] = []
    class Config():
        orm_mode = True

class Show_SubCategory_items(Items):
    sub_category: SubCategory
    category: Category

    class Config():
        orm_mode = True


class Show_breakfast(Breakfast):
    item: Items


class Show_lunch(Lunch):
    item: Items


class Show_dinner(Dinner):
    item: Items


# class Add_to_cart(BaseModel):
#     item_name :str
#     MRP :float
#     discount :float
#     tax :float
#     quantity:int
#     item_price : float
#     item_description :str
#     item_features :str
#     order_date = datetime.utcnow()
#     class Config():
#         orm_mode = True


# class place_order(Add_to_cart):
#     item_name :str
#     MRP :float
#     discount :float
#     tax :float
#     quantity:int
#     item_price : float
#     item_description :str
#     item_features :str
#     order_date = datetime.utcnow()
# class Show_cart(Items):
#         item:List[Items]=[]



class Ingredients(BaseModel):
    ingredient_name:str
    ing_quantity:float
    class Config():
        orm_mode = True

class Recipe(BaseModel):
    item_name:str
    class Config():
        orm_mode = True

class IngredientsForRecipe(BaseModel):
    ingredient_name:str
    ingredients_quantity:float
    class Config():
        orm_mode = True

class show_recipe(Recipe):
    ing:List[IngredientsForRecipe]=[]
    class Config():
        orm_mode = True



















class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[str] = None

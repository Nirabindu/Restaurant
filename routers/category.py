from fastapi import APIRouter, HTTPException, Depends, status, File, UploadFile
from sql_app import database, schemas, models
from sqlalchemy.orm import Session
from security import hashing, oauth2, tokens
from typing import List, Optional, Dict
import shortuuid
import shutil
#from fastapi.encoders import jsonable_encoder


router = APIRouter(tags=['Add Category'])


# adding Category

@router.post('/add_category')
def add_category(category_name: str, discount: Optional[float] = 0.0, db: Session = Depends(database.get_db), current_user: schemas.Users = Depends(oauth2.get_current_user), file: UploadFile = File(...)):

    category = db.query(models.Category).filter(
        models.Category.category_name == category_name).first()
    if category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'category already added')

    file.filename = f'{shortuuid.uuid()}.jpg'
    with open("static/images/category_img"+file.filename, 'wb') as img:
        shutil.copyfileobj(file.file, img)
    url = str("static/images/category_img/"+file.filename)

    new_category = models.Category(
        category_name=category_name,
        discount=discount,
        img=url
    )
    db.add(new_category)
    db.commit()
    db.refresh(new_category)
    return {'Category added'}


# adding subcategory

@router.post('/add_sub_category')
def add_subcategory(category_id: int, sub_category_name: str, db: Session = Depends(database.get_db), current_user: schemas.Users = Depends(oauth2.get_current_user), file: UploadFile = File(...)):

    cat_id = db.query(models.Category).filter(
        models.Category.category_id == category_id).first()
    if not cat_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f'Id not Found')
    subcat_name = db.query(models.SubCategory).filter(
        models.SubCategory.sub_category_name == sub_category_name).first()
    if subcat_name:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'sub catatony already added')

    file.filename = f'{shortuuid.uuid()}.jpg'
    with open("static/images/subcat_img/"+file.filename, 'wb') as img:
        shutil.copyfileobj(file.file, img)
    url = str("static\images\subcat_img/"+file.filename)

    new_sub_category = models.SubCategory(
        sub_category_name=sub_category_name,
        img=url,
        category_id=cat_id.category_id
    )
    db.add(new_sub_category)
    db.commit()
    db.refresh(new_sub_category)
    return {'category added'}


# adding items
@router.post('/add_items')
def addItem(sub_category_id: int, item_name: str, item_price: float, MRP: float, item_description: str, item_features: str, tax: float,discount: Optional[float] = 0.0, db: Session = Depends(database.get_db), current_user: schemas.Users = Depends(oauth2.get_current_user), file: List[UploadFile] = File(...)):

    subcategory_id = db.query(models.SubCategory).filter(
        sub_category_id == models.SubCategory.sub_category_id).first()
    category = db.query(models.Category).filter(models.SubCategory.category_id == models.Category.category_id).filter(
        sub_category_id == models.SubCategory.sub_category_id).first()
    itemsname = db.query(models.Items).filter(item_name == models.Items.item_name).filter(
        models.SubCategory.sub_category_id == sub_category_id).first()
    if itemsname:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Items in a particular sub category already added')

    new_item = models.Items(
        item_name=item_name,
        item_price=item_price,
        MRP=MRP,
        discount=discount,
        item_description=item_description,
        item_features=item_features,
        tax=tax,
        sub_cat_id=subcategory_id.sub_category_id,
        category_id=category.category_id
    )
    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    itemid = db.query(models.Items).filter(
        models.Items.item_name == item_name).first()
    for i in file:
        i.filename = f'{shortuuid.uuid()}.jpg'
        with open("static/images/item_img/"+i.filename, 'wb') as img:
            shutil.copyfileobj(i.file, img)
        url = str("static/images/item_img/"+i.filename)
        new_item_img = models.Item_img(
            item_img=url,
            item_id=itemid.item_id
        )
        db.add(new_item_img)
        db.commit()
        db.refresh(new_item_img)
    return {'Item Added'}


# grouping items
# grouping breakfast items

@router.post('/grouping_Items_breakfast /')
def breakfast_grouping(item_id: int, db: Session = Depends(database.get_db), current_user: schemas.Users = Depends(oauth2.get_current_user)):
    items_in_breakfast = db.query(models.Breakfast).filter(
        item_id == models.Breakfast.item_id).first()
    if items_in_breakfast:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Items in a Breakfast already added')

    items_id = db.query(models.Items).filter(
        item_id == models.Items.item_id).first()
    new_item = models.Breakfast(
        item_id=items_id.item_id

    )
    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    return{'adding to breakfast'}

# grouping items for Lunch


@router.post('/grouping_Items_Lunch /')
def lunch_grouping(item_id: int, db: Session = Depends(database.get_db), current_user: schemas.Users = Depends(oauth2.get_current_user)):
    items_in_Lunch = db.query(models.Lunch).filter(
        item_id == models.Lunch.item_id).first()
    if items_in_Lunch:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Items in a Lunch already added')

    items_id = db.query(models.Items).filter(
        item_id == models.Items.item_id).first()

    new_item = models.Lunch(
        item_id=items_id.item_id

    )
    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    return{'adding to lunch'}

# grouping items for Dinner


@router.post('/grouping_Items_Dinner /')
def dinner_grouping(item_id: int, db: Session = Depends(database.get_db), current_user: schemas.Users = Depends(oauth2.get_current_user)):
    items_in_Dinner = db.query(models.Dinner).filter(
        item_id == models.Dinner.item_id).first()
    if items_in_Dinner:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Items in a Lunch already added')

    items_id = db.query(models.Items).filter(
        item_id == models.Items.item_id).first()

    new_item = models.Dinner(
        item_id=items_id.item_id



    )
    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    return{'adding to Dinner'}


# show category

@router.get('/show_all_category/', response_model=List[schemas.Show_category])
def show_category(db: Session = Depends(database.get_db), current_user: schemas.Users = Depends(oauth2.get_current_user)):
    category = db.query(models.Category).all()
    return category
# Show subcategory with category


@router.get('/show_all_category_with_subCategory/', response_model=List[schemas.Show_category_sub_category])
def show_sub_category(db: Session = Depends(database.get_db), current_user: schemas.Users = Depends(oauth2.get_current_user)):
    allcatagory = db.query(models.Category).all()
    return allcatagory


# Show All Items

@router.get('/show_items/', response_model=List[schemas.Show_SubCategory_items])
def show_items(db: Session = Depends(database.get_db), current_user: schemas.Users = Depends(oauth2.get_current_user)):
    item = db.query(models.Items).filter(
        models.SubCategory.sub_category_id == models.Items.sub_cat_id).all()
    return item


# Show break fast Item
@router.get('/show_breakfast_item/', response_model=List[schemas.Show_breakfast])
def show_breakfast(db: Session = Depends(database.get_db), current_user: schemas.Users = Depends(oauth2.get_current_user)):
    breakfast = db.query(models.Breakfast).all()
    return breakfast


# show lunch Items
@router.get('/show_lunch_item/', response_model=List[schemas.Show_lunch])
def show_lunch(db: Session = Depends(database.get_db), current_user: schemas.Users = Depends(oauth2.get_current_user)):
    lunch = db.query(models.Lunch).all()
    return lunch


# show Dinner Items

@router.get('/show_Dinner_items/', response_model=List[schemas.Show_dinner])
def show_dinner(db: Session = Depends(database.get_db), current_user: schemas.Users = Depends(oauth2.get_current_user)):
    dinner = db.query(models.Dinner).all()
    return dinner


'''
# adding Items to cart
@router.post('/adding_items_to_cart/')
def addtocart(add_item_to_cart: int,quantity:int = 1, db: Session = Depends(database.get_db), current_user: schemas.Users = Depends(oauth2.get_current_user)):
    check_item = db.query(models.Add_to_cart).filter(models.Add_to_cart.item_id == add_item_to_cart).first()
    if not check_item:
        items = db.query(models.Items).filter(models.Items.item_id == add_item_to_cart).first()
        cart_item = models.Add_to_cart(
            item_id=items.item_id,
            item_name=items.item_name,
            MRP = items.MRP,
            discount = items.discount,
            tax=items.tax,
            quantity=quantity ,
            item_price=items.item_price * quantity,
            item_description=items.item_description,
            item_features=items.item_features
        )
        db.add(cart_item)
        db.commit()
        db.refresh(cart_item)
        return cart_item
    # else:
    #     item = db.query(models.Items).filter(models.Add_to_cart.item_id == add_item_to_cart).first()
    #     ck_item = db.query(models.Add_to_cart).filter(models.Add_to_cart.item_id == add_item_to_cart).first()
       
    #     ck_item.item_id=item.item_id,
    #     ck_item.item_name=item.item_name,
    #     ck_item.MRP = item.MRP,
    #     ck_item.discount = item.discount,
    #     ck_item.tax=item.tax,
    #     ck_item.quantity = ck_item.quantity+1,
    #     ck_item.item_price= 100,
    #     ck_item.item_description=item.item_description,
    #     ck_item.item_features=item.item_description
    #     db.commit()
    #     db.refresh(check_item)
    #    return



@router.get('/view_cart',response_model = List[schemas.place_order])
def view_cart(db: Session = Depends(database.get_db), current_user: schemas.Users = Depends(oauth2.get_current_user)):
    view = db.query(models.Add_to_cart).all()
    total_ammount = 0
    for i in view:
        total_ammount = total_ammount + i.item_price
    return view,total_ammount  



@router.delete('/delete_item_from_cart/',)
def delete_item_from_cart(cart_id:int,db: Session = Depends(database.get_db), current_user: schemas.Users = Depends(oauth2.get_current_user)):
    item = db.query(models.Add_to_cart).filter(cart_id == models.Add_to_cart.cart_id).first()
    db.delete(item)
    db.commit()
    return{'item remove from cart'}

@router.post('/place_order/')
def place_order(db: Session = Depends(database.get_db), current_user: schemas.Users = Depends(oauth2.get_current_user)):
    getting_items = db.query(models.Add_to_cart).all()
    total_ammount = 0
    for i in getting_items:
        total_ammount = total_ammount + i.item_price 
    billing = models.Billing(
        total_ammount = total_ammount
    )

    db.add(billing)
    db.commit()
    db.refresh(billing) 
    return billing


'''

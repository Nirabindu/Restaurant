from sqlalchemy import Column, String, Integer, BigInteger, ForeignKey, Boolean, DateTime, Float
from sqlalchemy.orm import relationship
from sql_app import database
import datetime


class Users(database.Base):
    __tablename__ = 'users'

    id = Column(BigInteger, primary_key=True, index=True)
    user_id = Column(String(45), unique=True)
    name = Column(String(45), nullable=False)
    email = Column(String(255), nullable=False)
    mobile_no = Column(BigInteger, nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    status = Column(Boolean, default=True)
    create_at = Column(DateTime, default=datetime.datetime.utcnow)


class Category(database.Base):
    __tablename__ = 'category'
    category_id = Column(BigInteger, primary_key=True, index=True)
    category_name = Column(String(50), nullable=False, unique=True)
    discount = Column(Float, nullable=False)
    status = Column(Boolean, default=True)
    img = Column(String(255))
    create_at = Column(DateTime, default=datetime.datetime.utcnow)
    sub = relationship('SubCategory', back_populates='cat')
    item = relationship('Items', back_populates='category')


class SubCategory(database.Base):
    __tablename__ = 'subcategory'
    sub_category_id = Column(BigInteger, primary_key=True, index=True)
    sub_category_name = Column(String(50), unique=True, nullable=False)
    status = Column(Boolean, default=True)
    create_at = Column(DateTime, default=datetime.datetime.utcnow)
    img = Column(String(255))
    category_id = Column(BigInteger, ForeignKey('category.category_id'))
    cat = relationship('Category', back_populates='sub')
    item = relationship('Items', back_populates='sub_category')


class Items(database.Base):
    __tablename__ = 'items'
    item_id = Column(BigInteger, primary_key=True, index=True)
    item_name = Column(String(50))
    item_price = Column(Float)
    item_description = Column(String(255))
    item_features = Column(String(100))
    status = Column(Boolean, default=True)
    avalability = Column(Boolean, default=True)
    tax = Column(Float, nullable=False)
    MRP = Column(Float, nullable=False)
    discount = Column(Float, nullable=False)
    create_at = Column(DateTime, default=datetime.datetime.utcnow)
    sub_cat_id = Column(BigInteger, ForeignKey('subcategory.sub_category_id'))
    category_id = Column(BigInteger, ForeignKey('category.category_id'))
    category = relationship('Category', back_populates='item')
    sub_category = relationship('SubCategory', back_populates='item')
    it_img = relationship('Item_img', back_populates='itemmg')
    breakfast = relationship('Breakfast', back_populates='item')
    lunch = relationship('Lunch', back_populates='item')
    dinner = relationship('Dinner', back_populates='item')
    #addcart = relationship('Add_to_cart', back_populates='item')


class Item_img(database.Base):
    __tablename__ = 'item_img'
    img_id = Column(BigInteger, primary_key=True, index=True)
    item_img = Column(String(255))
    item_id = Column(BigInteger, ForeignKey('items.item_id'))
    itemmg = relationship('Items', back_populates='it_img')


class Breakfast(database.Base):
    __tablename__ = 'breakfast'
    breakfast_id = Column(BigInteger, primary_key=True, index=True)
    item_id = Column(BigInteger, ForeignKey('items.item_id'))
    item = relationship('Items', back_populates='breakfast')


class Lunch(database.Base):
    __tablename__ = 'lunch'
    lunch_id = Column(BigInteger, primary_key=True, index=True)
    item_id = Column(BigInteger, ForeignKey('items.item_id'))
    item = relationship('Items', back_populates='lunch')


class Dinner(database.Base):
    __tablename__ = 'dinner'
    dinner_id = Column(BigInteger, primary_key=True, index=True)
    item_id = Column(BigInteger, ForeignKey('items.item_id'))
    item = relationship('Items', back_populates='dinner')

'''
class Add_to_cart(database.Base):
    __tablename__ = 'cart'
    cart_id = Column(BigInteger, primary_key=True, index=True)
    item_name = Column(String(50))
    item_price = Column(Float)
    item_description = Column(String(255))
    item_features = Column(String(100))
    status = Column(Boolean, default=True)
    avalability = Column(Boolean, default=True)
    tax = Column(Float, nullable=False)
    MRP = Column(Float, nullable=False)
    discount = Column(Float, nullable=False)
    quantity = Column(Integer, default=1)
    item_id = Column(BigInteger, ForeignKey('items.item_id'))
    item = relationship('Items', back_populates='addcart')
    # bill = relationship('Billing',back_populates='cart')

class Billing(database.Base):
    __tablename__='billing'
    billing_id = Column(BigInteger,primary_key = True,index=True)
    total_ammount = Column(Float)
    billing_date = Column(DateTime, default=datetime.datetime.utcnow)
    # cart_id = Column(BigInteger,ForeignKey('cart.cart_id'))
    #cart = relationship('Add_to_cart',back_populates='bill')
'''
class Ingredients(database.Base):
    __tablename__ = 'ingredients'
    ing_id = Column(BigInteger,primary_key = True, index = True)
    ingredient_name = Column(String(255),unique = True,nullable = False)
    ing_quantity = Column(Float)
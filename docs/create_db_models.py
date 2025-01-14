# created from response - used to create database and project
#  should run without error
#  if not, check for decimal, indent, or import issues

import decimal

import logging



logging.getLogger('sqlalchemy.engine.Engine').disabled = True  # remove for additional logging

import sqlalchemy



from sqlalchemy.sql import func  # end imports from system/genai/create_db_models_inserts/create_db_models_prefix.py

from logic_bank.logic_bank import Rule

from sqlalchemy import create_engine, ForeignKey, Column, Integer, String, Float, DateTime, Boolean, Table
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from sqlalchemy.sql import func
import datetime

Base = declarative_base()

# Table Definitions

class Customer(Base):
    """description: A table to store customer details."""
    __tablename__ = 'customers'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    balance = Column(Float, default=0.0)
    credit_limit = Column(Float, nullable=False)

class Order(Base):
    """description: A table to store order details, including a notes field."""
    __tablename__ = 'orders'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    customer_id = Column(Integer, ForeignKey('customers.id'), nullable=False)
    amount_total = Column(Float, default=0.0)
    date_shipped = Column(DateTime, nullable=True)
    notes = Column(String, nullable=True)
    
class Product(Base):
    """description: A table to store product details."""
    __tablename__ = 'products'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    unit_price = Column(Float, nullable=False)

class Item(Base):
    """description: A table to store items linked to orders and products."""
    __tablename__ = 'items'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey('orders.id'), nullable=False)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
    quantity = Column(Integer, nullable=False)
    amount = Column(Float, default=0.0)
    unit_price = Column(Float, nullable=False)
    
class Supplier(Base):
    """description: A table to store supplier details."""
    __tablename__ = 'suppliers'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)

class Inventory(Base):
    """description: A table to track inventory for each product."""
    __tablename__ = 'inventory'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
    quantity_in_stock = Column(Integer, nullable=False)
    reorder_level = Column(Integer, nullable=False)

class Category(Base):
    """description: A table to categorize products."""
    __tablename__ = 'categories'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)

class ProductCategory(Base):
    """description: A linking table for products and categories."""
    __tablename__ = 'product_categories'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
    category_id = Column(Integer, ForeignKey('categories.id'), nullable=False)

class CustomerReview(Base):
    """description: A table for storing customer reviews for products."""
    __tablename__ = 'customer_reviews'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
    customer_id = Column(Integer, ForeignKey('customers.id'), nullable=False)
    review_date = Column(DateTime, default=func.now())
    rating = Column(Integer, nullable=False)
    comment = Column(String, nullable=True)

class Address(Base):
    """description: A table to store addresses for customers."""
    __tablename__ = 'addresses'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    customer_id = Column(Integer, ForeignKey('customers.id'), nullable=False)
    street = Column(String, nullable=False)
    city = Column(String, nullable=False)
    state = Column(String, nullable=False)
    postal_code = Column(String, nullable=False)

class Payment(Base):
    """description: A table for storing payment details associated with orders."""
    __tablename__ = 'payments'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey('orders.id'), nullable=False)
    payment_date = Column(DateTime, default=func.now())
    amount_paid = Column(Float, nullable=False)

class Shipment(Base):
    """description: A table for storing shipment information related to orders."""
    __tablename__ = 'shipments'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey('orders.id'), nullable=False)
    shipment_date = Column(DateTime, nullable=True)
    shipped = Column(Boolean, default=False)

# Establish the database
engine = create_engine('sqlite:///system/genai/temp/create_db_models.sqlite')
Base.metadata.create_all(engine)

# Sample Data Insertion
Session = sessionmaker(bind=engine)
session = Session()

# Sample Customers
customers = [Customer(name=f"Customer {i+1}", credit_limit=1000.0 + i * 100) for i in range(5)]
session.add_all(customers)
session.commit()

# Sample Products
products = [Product(name=f"Product {i+1}", unit_price=10.0 + i * 5) for i in range(5)]
session.add_all(products)
session.commit()

# Sample Orders
orders = [Order(customer_id=customers[i % len(customers)].id, amount_total=0.0, date_shipped=None) for i in range(10)]
session.add_all(orders)
session.commit()

# Sample Items
for i in range(15):
    product = products[i % len(products)]
    item = Item(order_id=orders[i % len(orders)].id, product_id=product.id, quantity=2 + i,
                unit_price=product.unit_price, amount=(2 + i) * product.unit_price)
    session.add(item)
session.commit()

# Fill for other tables similarly (addresses, payments, shipments, etc. with basic data)

# Sample Address
addresses = [
    Address(customer_id=customers[i % len(customers)].id, street="Street A", city="City X", state="State Y", postal_code="12345")
    for i in range(len(customers))
]
session.add_all(addresses)
session.commit()

# Sample Payment
payments = [
    Payment(order_id=orders[i % len(orders)].id, amount_paid=orders[i % len(orders)].amount_total)
    for i in range(len(orders))
]
session.add_all(payments)
session.commit()

# Sample Inventory
inventory_items = [
    Inventory(product_id=product.id, quantity_in_stock=100, reorder_level=10) for product in products
]
session.add_all(inventory_items)
session.commit()

# Sample Category
categories = [Category(name=f"Category {i+1}") for i in range(5)]
session.add_all(categories)
session.commit()

# Sample ProductCategory (Linking Table)
product_categories = [
    ProductCategory(product_id=products[i % len(products)].id, category_id=categories[i % len(categories)].id)
    for i in range(15)
]
session.add_all(product_categories)
session.commit()

# Sample CustomerReview
reviews = [
    CustomerReview(product_id=products[i % len(products)].id, customer_id=customers[i % len(customers)].id, rating=4 + (i % 2))
    for i in range(15)
]
session.add_all(reviews)
session.commit()

# Sample Shipment
shipments = [
    Shipment(order_id=orders[i % len(orders)].id, shipped=True, shipment_date=datetime.datetime.now())
    for i in range(len(orders))
]
session.add_all(shipments)
session.commit()

# Declare Logic with LogicBank
def declare_logic():
    Rule.sum(derive=Customer.balance, as_sum_of=Order.amount_total, where=lambda row: row.date_shipped is None)
    Rule.sum(derive=Order.amount_total, as_sum_of=Item.amount)
    Rule.formula(derive=Item.amount, as_expression=lambda row: row.quantity * row.unit_price)
    Rule.copy(derive=Item.unit_price, from_parent=Product.unit_price)
    Rule.constraint(validate=Customer,
                    as_condition=lambda row: row.balance <= row.credit_limit,
                    error_msg="Customer balance ({row.balance}) exceeds credit limit ({row.credit_limit})")

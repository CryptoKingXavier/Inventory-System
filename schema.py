"""
Author: CryptoKingXavier
Title: New Inventory Item Schema
"""


# Importing required libraries
from uuid import uuid4
from datetime import datetime
from typing_extensions import Annotated
from typing import Mapping, Optional, Literal
from pydantic import BaseModel, StringConstraints


# Item Identification
class ID(BaseModel):
  item_name: str
  item_id: str = str(uuid4())   # unique identifier


# Description & Categorization
class Category(BaseModel):
  category: str
  description: Annotated[str, StringConstraints(max_length=50)]


# Quantity Management
class QtyMgt(BaseModel):
  qty: int = 1
  threshold: int = 3   # reorder alert trigger


#Pricing
class Pricing(BaseModel):
  currency: Annotated[str, StringConstraints(max_length=3, to_upper=True)]
  cost_price: float   # for profit margins
  unit_price: float
  discount: Optional[float] = float()


# Supplier Information
class SupplierInfo(BaseModel):
  supplier_name: str
  supplier_info: Optional[Mapping[str, str]] = {"email": str(), "phone": str()}


# Storage Location
class Storage(BaseModel):
  store_location: Annotated[str, StringConstraints(max_length=50)]
  zone: Optional[str] = str()


# Date Information
class DateInfo(BaseModel):
  expiry_date: Optional[str] = str()
  date_added: str = datetime.now().date().isoformat()
  time_added: str = datetime.now().time().isoformat()


# Additional Attributes
class Extras(BaseModel):
  weight: str
  dimensions: Optional[str] = str()
  barcode: Optional[str] = str()
  nafdac: Optional[str] = str()


# Status
class Status(BaseModel):
  item_status: Literal["ACTIVE", "OUT-OF-STOCK"]


# Function to compute all instance variables
def initialize_data():
  return {
    "id": ID(item_name=input("Name: ").strip()),
    "category": Category(
      category=input("Category: ").strip(),
      description=input("Description: ").strip()
    ),
    "qty_mgt": QtyMgt(qty=int(input("Initial Quantity: ").strip())),
    "pricing": Pricing(
      currency=input("Base Currency: ").strip(),
      cost_price=float(input("Cost Price: ").strip()),
      unit_price=float(input("Unit Price: ").strip()),
      discount=float(input("Optional Discount: ").strip())
    ),
    "supplier_info": SupplierInfo(
      supplier_name=input("Supplier's Name: ").strip(),
      supplier_info={
        "email": input("Supplier Email: ").strip(),
        "phone": input("Supplier Number: ").strip()
      }
    ),
    "storage": Storage(
      store_location=input("Store Location: ").strip(),
      zone=input("Optional Zone: ").strip()
    ),
    "date_info": DateInfo(expiry_date=input("Optional Expiry Date: ").strip()),
    "extras": Extras(
      weight=input('Weight: ').strip(),
      dimensions=input("Optional Dimensions: ").strip(),
      barcode=input("Optional Barcode Number: ").strip(),
      nafdac=input("Optional NAFDAC Reg. No: ").strip()
    ),
    "status": Status(item_status=input("Status [ACTIVE|OUT-OF-STOCK]: ").upper().strip())
  }


def model(schema):
  return {
    "category": {
        "category": schema.get("category"),
        "description": schema.get("description")
    },
    "date_info": {
        "date_added": schema.get("date_added"),
        "expiry_date": schema.get("expiry_date"),
        "time_added": schema.get("time_added")
    },
    "extras": {
        "barcode": schema.get("barcode"),
        "dimensions": schema.get("dimensions"),
        "nafdac": schema.get("nafdac"),
        "weight": schema.get("weight")
    },
    "id": {
        "item_id": schema.get("item_id"),
        "item_name": schema.get("item_name")
    },
    "pricing": {
        "cost_price": schema.get("cost_price"),
        "currency": schema.get("currency"),
        "discount": schema.get("discount"),
        "unit_price": schema.get("unit_price")
    },
    "qty_mgt": {
        "qty": schema.get("qty"),
        "threshold": schema.get("threshold")
    },
    "status": {
        "item_status": schema.get("item_status")
    },
    "storage": {
        "store_location": schema.get("store_location"),
        "zone": schema.get("zone")
    },
    "supplier_info": {
        "supplier_info": {
            "email": schema.get("supplier_info").get("email"),
            "phone": schema.get("supplier_info").get("phone")
        },
        "supplier_name": schema.get("supplier_name")
    }
  }
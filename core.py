"""
Author: CryptoKingXavier
Title: Inventory Core Functionalities
"""


# Importing required libraries
from schema import *
from pydantic import BaseModel
from tinydb import Query, TinyDB
from typing import Optional, Union


# TinyDB instance
USER = Query()
DB = TinyDB("inventory.json")


# Retrieving inventory items
def get_inventory(): return DB.all()


# Retrieving inventory items ids
def get_inventory_ids():
  return [item.get("id").get("item_id") for item in get_inventory()]


# Add Item: add new items to the inventory
class AddItem:
  id: Optional[Union[ID, None]] = None
  extras: Optional[Union[Extras, None]] = None
  status: Optional[Union[Status, None]] = None
  qty_mgt: Optional[Union[QtyMgt, None]] = None
  pricing: Optional[Union[Pricing, None]] = None
  storage: Optional[Union[Storage, None]] = None
  category: Optional[Union[Category, None]] = None
  date_info: Optional[Union[DateInfo, None]] = None
  supplier_info: Optional[Union[SupplierInfo, None]] = None
  
  def initialize_fields(self):
    data = initialize_data()
    for key, value in data.items():
      setattr(self, key, value)


# View Inventory: display all items and filter based on categories
class ViewInventory(BaseModel):
  def view(self, id = None):
    if not id:
      id: str = input("Item ID: ").strip()
    
    if id in get_inventory_ids():
      return DB.search(USER.id.item_id == id)
    else:
      raise KeyError(f"⚠️ No item found with ID: {id}❗")


# Update Item: modify an item’s information
class UpdateItem(BaseModel):
  def update(self):
    id: str = input("Item ID: ").strip()
    if id in get_inventory_ids():
      return id, ViewInventory().view(id)
    else:
      raise KeyError(f"⚠️ No item found with ID: {id}❗")


# Delete Item: remove items that are no longer needed or relevant
class DeleteItem(BaseModel):
  def delete(self):
    id: str = input("Item ID: ").strip()
    if id in get_inventory_ids():
      DB.remove(USER.id.item_id == id)
      print(f"ℹ️ Item with ID: {id} trashed... 🗑️")
    else:
      raise KeyError(f"⚠️ Item with ID: {id} not found❗")

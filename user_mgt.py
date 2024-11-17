"""
Author: CryptoKingXavier
Title: Inventory User Management
"""


# Importing required libraries
from yaml import dump
from time import sleep
from schema import model
from core import AddItem, DB, DeleteItem, UpdateItem, USER, ViewInventory, get_inventory


# Empty Inventory Error
class InventoryError(Exception):
  def __init__(self, error: str):
    super().__init__(error)


class Alerts:
  # Custom reorder alerts
  def generate_reorder_alert(self, item_name: str, id: str, current_quantity: int, reorder_threshold: int):
    return f"""
    🔔 REORDER ALERT 🔔
    Item: {item_name}
    Item ID: {id}
    Current Quantity: {current_quantity}
    Reorder Threshold: {reorder_threshold}
    
    Action Required: Please reorder this item
    immediately to maintain optimal stock levels.
    """
  
  def reorder(self):
    """Setting threshold for low-stock items when inventory levels fall below a certain quantity"""
    inventory = get_inventory()
    
    if inventory:
      for item in inventory:
        threshold = item.get("qty_mgt").get("threshold")
        if item.get("qty_mgt").get("qty") < threshold:
          print(self.generate_reorder_alert(
            reorder_threshold=threshold,
            id=item.get("id").get("item_id"),
            item_name=item.get("id").get("item_name"),
            current_quantity=item.get("qty_mgt").get("qty")
          ))
    else:
      raise InventoryError("⚠️ Inventory is empty❗")


# Staff level access
class Staff:
  # Inventory Alerts
  def alerts(self): Alerts().reorder()
  
  # Viewing privilege
  def viewInventory(self, id = None):
    item = ViewInventory().view(id) if id else ViewInventory().view()
    print(f"\nRetrieving Item Details...⏳"); sleep(3)
    print(dump(item, default_flow_style=False, sort_keys=False))


# Admin level access
class Admin(Staff):
  # Creating privilege
  def addItem(self):   
    new_item = AddItem()
    new_item.initialize_fields()
    DB.insert(model(schema={
      **new_item.id.model_dump(),
      **new_item.category.model_dump(),
      **new_item.qty_mgt.model_dump(),
      **new_item.pricing.model_dump(),
      **new_item.supplier_info.model_dump(),
      **new_item.storage.model_dump(),
      **new_item.date_info.model_dump(),
      **new_item.extras.model_dump(),
      **new_item.status.model_dump()
    }))
    print(f"ℹ️ Item with ID: {new_item.id.item_id} created successfully❗")
  
  # Deleting privilege
  def deleteItem(self): DeleteItem().delete()
    
  # Updating privilege
  def updateItem(self):
    id, item = UpdateItem().update()
    item = item[0]
    super().viewInventory(id)
    
    # Updating item
    print(f"\nUpdating Item Details... ♻️")
    print(f"First Level Keys\n\t{item.keys()}")
    first_level_key = input("First Level Key: ").strip()
    if first_level_key in item.keys():
      print(f"\nSecond Level Keys\n\t{item.get(first_level_key).keys()}")
      second_level_key = input("Second Level Key: ").strip()
      if second_level_key in item.get(first_level_key).keys():
        match second_level_key:
          case "supplier_info":
            print(f"\nThird Level Keys\n\t{item.get(first_level_key).get(second_level_key).keys()}")
            third_level_key = input("Third Level Key: ").strip()
            new_entry = input(f"New {third_level_key.title()}: ").strip()
            item[first_level_key][second_level_key][third_level_key] = new_entry
          case "item_id":
            print("⚠️ Immutable Item ID❗")
          case "threshold":
            print("⚠️ Immutable Item Threshold❗")
          case "qty":
            entry = int(input(f"New {second_level_key.title()}: ").strip())
            item[first_level_key][second_level_key] = entry
          case "cost_price" | "unit_price" | "discount":
            entry = float(input(f"New {second_level_key.title()}: ").strip())
            item[first_level_key][second_level_key] = entry
          case _:
            entry = input(f"New {second_level_key.title()}: ").strip()
            item[first_level_key][second_level_key] = entry
    
    # Updating in database
    DB.update(item, USER.id.item_id == id)
    print(f"ℹ️ Item with ID: {id} updated successfully❗")
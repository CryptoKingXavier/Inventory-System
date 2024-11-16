"""
Author: CryptoKingXavier
Title: Inventory Control
"""


# Importing required libraries
from core import get_inventory
from pydantic import BaseModel


# Empty Inventory Error
class InventoryError(Exception):
  def __init__(self, error: str):
    super().__init__(error)


# Custom reorder alerts
def generate_reorder_alert(item_name: str, id: str, current_quantity: int, reorder_threshold: int):
  return f"""
  🔔 REORDER ALERT 🔔
  Item: {item_name}
  Item ID: {id}
  Current Quantity: {current_quantity}
  Reorder Threshold: {reorder_threshold}
  
  Action Required: Please reorder this item
  immediately to maintain optimal stock levels.
  """


class Alerts(BaseModel):
  def reorder(self):
    """Setting threshold for low-stock items when inventory levels fall below a certain quantity"""
    inventory = get_inventory()
    
    if inventory:
      for item in inventory:
        threshold = item.get("qty_mgt").get("threshold")
        if item.get("qty_mgt").get("qty") < threshold:
          print(generate_reorder_alert(
            reorder_threshold=threshold,
            id=item.get("id").get("item_id"),
            item_name=item.get("id").get("item_name"),
            current_quantity=item.get("qty_mgt").get("qty")
          ))
    else:
      raise InventoryError("⚠️ Inventory is empty❗")

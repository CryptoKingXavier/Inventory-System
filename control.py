"""
Author: CryptoKingXavier
Title: Inventory Control
"""


# Importing required libraries
from user_mgt import Admin


class Menu:
  def __init__(self):
    self.admin: Admin = Admin()
  
  def menu(self):
    while True:
      self.display_menu()
      choice = input("Enter your choice (1-5): ").strip()
      
      match choice:
        case "1": self.admin.addItem()
        case "2": self.admin.viewInventory()
        case "3": self.admin.updateItem()
        case "4": self.admin.deleteItem()
        case "5": self.admin.alerts()
        case "6":
          print("Exiting the application. Goodbye❗")
          break
        case _:
          print("Invalid choice. Please enter a number between 1 and 6.\n")
    
  @staticmethod
  def display_menu():
    print("""
    ==== Inventory System Menu ====
    1. Add Item
    2. View Inventory
    3. Update Item
    4. Delete Item
    5. Alerts
    6. Exit
    """)

from datetime import datetime

class Asset:
    def __init__(self, name, price, available_qty):
        self.name = name.upper()
        self.price = float(price) 
        self.available_qty = int(available_qty)
        
class PortfolioItem:
    def __init__(self, asset_name, quantity, buy_price):
        self.asset_name = asset_name
        self.quantity = int(quantity)
        self.buy_price = float(buy_price)
        
    @property
    def avarage_buy_price(self):
        return self.total_cost / self.quantity if self.quantity > 0 else 0
    
class TransactionRecord:
    def __init__(self, action, asset_name, quantity, price):
        self.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.action = action
        self.asset_name = asset_name
        self.quantity = int(quantity)
        self.price = float(price)
        
    def __str__(self):
        return f"[{self.timestamp}] {self.action} {self.asset_name} | Qty: {self.quantity} @ ${self.price: .2f}"
        
        
"""acts as the data blueprint for objects inside our engine""" 
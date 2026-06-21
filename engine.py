"""acts as my executable file. It catches unexpected runtime bugs (such as typing text for numeric inputs) and routes flow cleanly."""
from models import Asset, PortfolioItem, TransactionRecord

class TradingEngine:
    def __init__(self):
        self.balance = 100000.0
        self.history = []   #List of TransactionRecord objects
        self.portfolio = {}   # Key: asset_name, Value: PortfolioItem object
        
        
        # Initialize default mock market data
        self.market = {
            "GOLD": Asset("GOLD", 200.0, 500),
            "OIL": Asset("OIL", 50.0, 1000),
            "APPLE": Asset("APPLE", 180.0, 300),
            "TESLA": Asset("TESLA", 300.0, 200),
            "BITCOIN": Asset("BITCOIN", 65000.0, 50)
        }  
        
    def display_market(self):
        print("\n=== 📈 LIVE MARKET DATA ===")
        print(f"{'Asset':<10} | {'Current Price':<15} | {'Available Vol':<15}")
        print("-" * 46)
        for asset in self.market.values():
            print(f"{asset.name:<10} | ${asset.price:<14.2f} | {asset.available_qty:<15}")
            
    def buy_asset(self, asset_name, qty):
        asset_name = asset_name.upper()
        
        
          # 1. Validation Checks
        if asset_name not in self.market:
            print("❌ Transaction Rejected: Asset does not exist in this market.")
            return
        
        asset = self.market[asset_name]
        if qty <= 0:
            print("❌ Transaction Rejected: Quantity must be greater than zero.")
            return
        if qty >asset.available_qty:
            print(f"❌ Transaction Rejected: Market only has {asset.available_qty} units available.")
            return
        
        total_cost = qty * asset.price
        if total_cost > self.balance:
            print(f"❌ Transaction Rejected: Insufficient balance. Cost: ${total_cost:.2f} | Available: ${self.balance:.2f}")
            return
        
        # 2. Execute Transaction
        self.balance -= total_cost
        asset.available_qty -= qty
        
        
        # Update Portfolio
        if asset_name in self.portfolio:
            self.portfolio[asset_name].quantity += qty
            self.portfolio[asset_name].total_cost += total_cost
        else:
            self.portfolio[asset_name] = PortfolioItem(asset_name, qty, asset.price)
            
            
        # Log History
        # Log History
        self.history.append(TransactionRecord("BUY", asset_name, qty, asset.price))
        print(f"✅ Successfully bought {qty} units of {asset_name} for ${total_cost:.2f}")

    def sell_asset(self, asset_name, qty):
        asset_name = asset_name.upper()

        # 1. Validation Checks
        if asset_name not in self.portfolio or self.portfolio[asset_name].quantity == 0:
            print(f"❌ Transaction Rejected: You do not own any shares of {asset_name}.")
            return
        
        owned_item = self.portfolio[asset_name]
        if qty <= 0:
            print("❌ Transaction Rejected: Quantity must be greater than zero.")
            return
        if qty > owned_item.quantity:
            print(f"❌ Transaction Rejected: You cannot sell more than you own. Position size: {owned_item.quantity}")
            return

        # 2. Execute Transaction
        asset = self.market[asset_name]
        total_credit = qty * asset.price
        
        # Reduce total cost basis proportionally upon selling
        avg_cost = owned_item.average_buy_price
        owned_item.quantity -= qty
        owned_item.total_cost -= (qty * avg_cost)

        self.balance += total_credit
        asset.available_qty += qty

        # Clean up empty positions
        if owned_item.quantity == 0:
            del self.portfolio[asset_name]

        # Log History
        self.history.append(TransactionRecord("SELL", asset_name, qty, asset.price))
        print(f"✅ Successfully sold {qty} units of {asset_name} for ${total_credit:.2f}")

    def display_portfolio(self):
        print("\n=== 💼 YOUR PORTFOLIO ===")
        print(f"Account Liquidity (Cash): ${self.balance:.2f}")
        print("-" * 75)
        
        if not self.portfolio:
            print("Your portfolio is currently empty.")
            return

        headers = f"{'Asset':<10} | {'Qty':<6} | {'Avg Buy Px':<12} | {'Current Px':<12} | {'P&L ($)':<12}"
        print(headers)
        print("-" * 75)

        total_pnl = 0.0
        for item in self.portfolio.values():
            current_price = self.market[item.asset_name].price
            # Profit / Loss calculation: Qty * (Current Price - Average Buy Price)
            pnl = item.quantity * (current_price - item.average_buy_price)
            total_pnl += pnl
            
            pnl_str = f"${pnl:+.2f}"
            print(f"{item.asset_name:<10} | {item.quantity:<6} | ${item.average_buy_price:<11.2f} | ${current_price:<11.2f} | {pnl_str:<12}")
            
        print("-" * 75)
        print(f"Total Portfolio Unrealized P&L: ${total_pnl:+.2f}")

    def display_history(self):
        print("\n=== 📜 TRANSACTION HISTORY ===")
        if not self.history:
            print("No transactions executed yet.")
            return
        for record in self.history:
            print(record)
            
            
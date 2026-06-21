"""This acts as your executable file. It catches unexpected runtime bugs (such as typing text for numeric inputs) and routes flow cleanly."""

from engine import TradingEngine

def main():
    engine = TradingEngine()
    print("====== Welcome to Wise Command-Line Trading Simulation ======")

    while True:
        try:
            print("\n--- Main Menu ---")
            print("1. View Market\n2. Buy Asset\n3. Sell Asset\n4. View Portfolio\n5. Transaction History\n6. Exit")
            choice = input("Select an option (1-6): ").strip()

            if choice == "1":
                engine.display_market()
            
            elif choice == "2":
                asset = input("Enter asset name to BUY (e.g., TESLA): ").strip()
                qty = int(input("Enter target purchase quantity: "))
                engine.buy_asset(asset, qty)

            elif choice == "3":
                asset = input("Enter asset name to SELL (e.g., GOLD): ").strip()
                qty = int(input("Enter target liquidation quantity: "))
                engine.sell_asset(asset, qty)

            elif choice == "4":
                engine.display_portfolio()

            elif choice == "5":
                engine.display_history()

            elif choice == "6":
                print("\nExiting session. Finalizing ledger... Goodbye!")
                break
            else:
                print("❌ Invalid menu choice. Please input an integer from 1 to 6.")

        except ValueError:
            print("❌ Input Error: Quantities must be whole numbers. Please try again from where you left off.")
        except Exception as e:
            print(f"⚠️ Unforeseen system exception encountered: {e}")
            print("Your secure trading session has been preserved. Returning to main menu...")

if __name__ == "__main__":
    main()
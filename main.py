import time
from engine import TradingEngine

def secure_input(prompt, expected_type="string"):
    """
    Custom input handler that enforces correct data types.
    Allows up to 3 sequential failed attempts before locking out the user for 10 seconds.
    """
    attempts = 0
    while True:
        user_input = input(prompt).strip()
        
        if expected_type == "string":
            # For Asset Names: Must contain text and not be completely blank
            if user_input and user_input.isalpha():
                return user_input
            else:
                print("❌ Error: Invalid entry. Asset names must contain alphabetic characters only.")
                
        elif expected_type == "numeric_string":
            # For Main Menu choices: Must be a pure string of whole digits
            if user_input and user_input.isdigit():
                return user_input
            else:
                print("❌ Error: Invalid entry. Please input a valid whole number digit.")

        elif expected_type == "int":
            # For Quantities: Must parse correctly into a non-negative whole integer
            try:
                qty_val = int(user_input)
                if qty_val > 0:
                    return qty_val
                else:
                    print("❌ Error: Quantity must be a whole number greater than zero.")
            except ValueError:
                print("❌ Error: Invalid entry. Quantities must be whole digits only.")

        # If it falls through the type conditions above, count it as a strike
        attempts += 1
        if attempts >= 3:
            print("\n⛔ Too many invalid attempts! Please wait 10 seconds before trying again...")
            time.sleep(10)
            attempts = 0  # Reset mistake counter after timeout completes

def main():
    engine = TradingEngine()
    print("====== Welcome to Wisede Command-Line Trading Simulation ======")

    while True:
        try:
            print("\n--- Main Menu ---")
            print("1. View Market\n2. Buy Asset\n3. Sell Asset\n4. View Portfolio\n5. Transaction History\n6. Exit")
            
            # CHANGED: Using secure_input for safe menu choices
            choice = secure_input("Select an option (1-6): ", expected_type="numeric_string")

            if choice == "1":
                engine.display_market()
            
            elif choice == "2":
                # CHANGED: Added strict input validation for assets and whole-number quantities
                asset = secure_input("Enter asset name to BUY (e.g., TESLA): ", expected_type="string")
                qty = secure_input("Enter target purchase quantity: ", expected_type="int")
                engine.buy_asset(asset, qty)

            elif choice == "3":
                # CHANGED: Added strict input validation for liquidations
                asset = secure_input("Enter asset name to SELL (e.g., GOLD): ", expected_type="string")
                qty = secure_input("Enter target liquidation quantity: ", expected_type="int")
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

        except Exception as e:
            # Main fallback safety blanket to preserve engine data
            print(f"⚠️ Unforeseen system exception encountered: {e}")
            print("Your secure trading session has been preserved. Returning to main menu...")

if __name__ == "__main__":
    main()
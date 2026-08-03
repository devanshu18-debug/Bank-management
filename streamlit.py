
"""
Bank Account Management System
A cleaned-up, bug-fixed rewrite of a simple JSON-backed console banking app.
"""
 
import json
import random
import string
from pathlib import Path
 
 
# ---------------------------------------------------------------------------
# Small input helpers (keep validation logic out of the main class methods)
# ---------------------------------------------------------------------------
 
def ask_int(prompt, min_value=None, max_value=None):
    """Repeatedly prompt until a valid integer (optionally bounded) is given."""
    while True:
        raw = input(prompt).strip()
        try:
            value = int(raw)
        except ValueError:
            print("Please enter a whole number.")
            continue
        if min_value is not None and value < min_value:
            print(f"Value must be at least {min_value}.")
            continue
        if max_value is not None and value > max_value:
            print(f"Value must be at most {max_value}.")
            continue
        return value
 
 
def ask_nonempty(prompt):
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("This field can't be empty.")
 
 
def ask_pin(prompt):
    """Pin is kept as a string so leading zeros (e.g. '0142') aren't lost."""
    while True:
        pin = input(prompt).strip()
        if pin.isdigit() and len(pin) == 4:
            return pin
        print("Pin must be exactly 4 digits.")
 
 
def ask_email(prompt):
    while True:
        email = input(prompt).strip()
        if "@" in email and "." in email.split("@")[-1]:
            return email
        print("Please enter a valid email address.")
 
 
# ---------------------------------------------------------------------------
# Bank
# ---------------------------------------------------------------------------
 
class Bank:
    DB_FILE = "data.json"
 
    def __init__(self):
        self.data = self._load()
 
    # -- persistence ---------------------------------------------------
 
    def _load(self):
        path = Path(self.DB_FILE)
        if not path.exists():
            print("No existing data file found, starting fresh.")
            return []
        try:
            with open(path) as file:
                content = file.read().strip()
                return json.loads(content) if content else []
        except (json.JSONDecodeError, OSError) as err:
            print(f"Could not read data file ({err}); starting with empty data.")
            return []
 
    def _save(self):
        with open(self.DB_FILE, "w") as file:
            json.dump(self.data, file, indent=2)
 
    # -- helpers ---------------------------------------------------------
 
    @staticmethod
    def _generate_account_number():
        alpha = random.choices(string.ascii_letters, k=3)
        num = random.choices(string.digits, k=3)
        spchar = random.choices("!@#$%&*^", k=1)
        chars = alpha + num + spchar
        random.shuffle(chars)
        return "".join(chars)
 
    def _find_account(self, accnumber, pin):
        matches = [i for i in self.data if i["accountNO."] == accnumber and i["pin"] == pin]
        return matches[0] if matches else None
 
    def _authenticate(self):
        """Prompt for account number + pin, return the account dict or None."""
        accnumber = ask_nonempty("Please tell your account number: ")
        pin = input("Please tell your pin: ").strip()
        account = self._find_account(accnumber, pin)
        if account is None:
            print("Sorry, no matching account found.")
        return account
 
    # -- public operations -------------------------------------------------
 
    def create_account(self):
        print("\n--- Create Account ---")
        name = ask_nonempty("Tell me your name: ")
        age = ask_int("Tell me your age: ", min_value=0, max_value=120)
        if age < 18:
            print("Sorry, you must be at least 18 years old to create an account.")
            return
 
        email = ask_email("Tell me your email: ")
        pin = ask_pin("Choose a 4 digit pin: ")
 
        info = {
            "name": name,
            "age": age,
            "email": email,
            "pin": pin,
            "accountNO.": self._generate_account_number(),
            "balance": 0,
        }
 
        self.data.append(info)
        self._save()
 
        print("\nAccount created successfully! Please note down your account number.")
        for key, value in info.items():
            print(f"{key} : {value}")
 
    def deposit_money(self):
        print("\n--- Deposit Money ---")
        account = self._authenticate()
        if account is None:
            return
 
        amount = ask_int("How much do you want to deposit? ", min_value=1, max_value=10000)
        account["balance"] += amount
        self._save()
        print(f"Amount deposited successfully. New balance: {account['balance']}")
 
    def withdraw_money(self):
        print("\n--- Withdraw Money ---")
        account = self._authenticate()
        if account is None:
            return
 
        amount = ask_int("How much do you want to withdraw? ", min_value=1, max_value=10000)
        if account["balance"] < amount:
            print("Insufficient balance.")
            return
 
        account["balance"] -= amount
        self._save()
        print(f"Amount withdrawn successfully. New balance: {account['balance']}")
 
    def show_details(self):
        print("\n--- Account Details ---")
        account = self._authenticate()
        if account is None:
            return
 
        for key, value in account.items():
            print(f"{key} : {value}")
 
    def update_details(self):
        print("\n--- Update Account Details ---")
        account = self._authenticate()
        if account is None:
            return
 
        print("You cannot change age, account number, or balance here.")
        print("Leave a field blank to keep it unchanged.")
 
        new_name = input(f"New name (current: {account['name']}): ").strip()
        new_email = input(f"New email (current: {account['email']}): ").strip()
        new_pin = input("New 4 digit pin (leave blank to keep current): ").strip()
 
        changed = False
 
        if new_name:
            account["name"] = new_name
            changed = True
 
        if new_email:
            if "@" in new_email and "." in new_email.split("@")[-1]:
                account["email"] = new_email
                changed = True
            else:
                print("New email looked invalid, so it was not changed.")
 
        if new_pin:
            if new_pin.isdigit() and len(new_pin) == 4:
                account["pin"] = new_pin
                changed = True
            else:
                print("New pin must be exactly 4 digits, so it was not changed.")
 
        if changed:
            self._save()
            print("Details updated successfully.")
        else:
            print("No changes made.")
 
    def delete_account(self):
        print("\n--- Delete Account ---")
        account = self._authenticate()
        if account is None:
            return
 
        choice = input("Press Y to confirm deletion, any other key to cancel: ").strip().lower()
        if choice != "y":
            print("Deletion cancelled.")
            return
 
        self.data.remove(account)
        self._save()
        print("Account deleted successfully.")
 
 
# ---------------------------------------------------------------------------
# Main menu
# ---------------------------------------------------------------------------
 
MENU = """
========== Bank Account Management System ==========
1. Create Account
2. Deposit Money
3. Withdraw Money
4. View Account Details
5. Update Account Details
6. Delete Account
7. Exit
"""
 
 
def main():
    bank = Bank()
    print(MENU)
 
    actions = {
        1: bank.create_account,
        2: bank.deposit_money,
        3: bank.withdraw_money,
        4: bank.show_details,
        5: bank.update_details,
        6: bank.delete_account,
    }
 
    while True:
        choice = ask_int("Enter your choice (1-7): ", min_value=1, max_value=7)
 
        if choice == 7:
            print("Thank you for using the Bank Account Management System.")
            break
 
        action = actions[choice]
        try:
            action()
        except Exception as err:
            # Keep the app alive even if something unexpected happens.
            print(f"Something went wrong: {err}")
 
 
if __name__ == "__main__":
    main()
# python -m streamlit run app.py
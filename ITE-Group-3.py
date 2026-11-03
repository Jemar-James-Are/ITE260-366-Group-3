from datetime import date

items = []        
LOW_STOCK = 5      

def show_menu():
    print()
    print("=== VETERINARY INVENTORY MONITORING SYSTEM ===")
    print("1. Add item")
    print("2. Stock in")
    print("3. Stock out")
    print("4. View all items")
    print("5. Check alerts (low stock / expiring)")
    print("6. Exit")

def find_item(name):
    for item in items:
        if item["name"].lower() == name.lower():
            return item
    return None

def get_number(message):
    while True:
        value = input(message)
        if value.isdigit():
            return int(value)
        print("Please enter a whole number.")

def add_item():
    name = input("Item name: ")
    if name == "":
        print("Name cannot be empty.")
        return
    if find_item(name) is not None:
        print("That item already exists. Use Stock in instead.")
        return
    category = input("Category (medicine / vaccine / supply): ")
    qty = get_number("Starting quantity: ")
    expiry = input("Expiry date (YYYY-MM-DD, or press Enter if none): ")

    item = {"name": name, "category": category, "qty": qty, "expiry": expiry}
    items.append(item)
    print(name, "was added.")

def stock_in():
    name = input("Item name: ")
    item = find_item(name)
    if item is None:
        print("Item not found.")
        return
    amount = get_number("Quantity received: ")
    item["qty"] += amount
    print("Done. New quantity of", item["name"], "is", item["qty"])

def stock_out():
    name = input("Item name: ")
    item = find_item(name)
    if item is None:
        print("Item not found.")
        return
    amount = get_number("Quantity used: ")
    if amount > item["qty"]:
        print("Not enough stock! Only", item["qty"], "left.")
    else:
        item["qty"] -= amount
        print("Done. Remaining quantity of", item["name"], "is", item["qty"])

def view_items():
    if len(items) == 0:
        print("No items yet.")
        return
    print()
    print("Name".ljust(20), "Category".ljust(12), "Qty".ljust(6), "Expiry")
    print("-" * 52)
    for item in items:
        print(item["name"].ljust(20), item["category"].ljust(12),
              str(item["qty"]).ljust(6), item["expiry"])

def check_alerts():
    today = date.today()
    found = False
    for item in items:
        if item["qty"] <= LOW_STOCK:
            print("LOW STOCK:", item["name"], "- only", item["qty"], "left")
            found = True
        if item["expiry"] != "":
            try:
                parts = item["expiry"].split("-")
                exp = date(int(parts[0]), int(parts[1]), int(parts[2]))
            except (ValueError, IndexError):
                print("Check the expiry date format of", item["name"])
                continue
            days_left = (exp - today).days
            if days_left < 0:
                print("EXPIRED:", item["name"], "expired on", item["expiry"])
                found = True
            elif days_left <= 30:
                print("EXPIRING SOON:", item["name"], "in", days_left, "days")
                found = True
    if not found:
        print("No alerts. Everything looks good!")

# ---------- main program ----------
while True:
    show_menu()
    choice = input("Enter your choice (1-6): ")

    if choice == "1":
        add_item()
    elif choice == "2":
        stock_in()
    elif choice == "3":
        stock_out()
    elif choice == "4":
        view_items()
    elif choice == "5":
        check_alerts()
    elif choice == "6":
        print("Goodbye!")
        break
    else:
        print("Invalid choice. Please type a number from 1 to 6.")

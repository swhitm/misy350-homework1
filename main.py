# ============================================
# Coffee Shop Kiosk Inventory & Orders (CRUD)
# ============================================

# -----------------------------
# Starter Inventory Data
# -----------------------------
inventory = [
    {"item_id": 1, "name": "Espresso", "unit_price": 2.50, "stock": 40},
    {"item_id": 2, "name": "Latte", "unit_price": 4.25, "stock": 25},
    {"item_id": 3, "name": "Cold Brew", "unit_price": 3.75, "stock": 30},
    {"item_id": 4, "name": "Mocha", "unit_price": 4.50, "stock": 20},
    {"item_id": 5, "name": "Blueberry Muffin", "unit_price": 2.95, "stock": 18},
]

# -----------------------------
# Starter Orders Data
# -----------------------------
orders = [
    {"order_id": "Order_101", "item_id": 2, "quantity": 2, "status": "Placed", "total": 8.50},
    {"order_id": "Order_102", "item_id": 3, "quantity": 1, "status": "Placed", "total": 3.75},
]

# ==========================================================
# READ
# ==========================================================

# Query 0: View all items in the inventory with stock less than 20.

# 1. Input:
threshold = 20

# 2. Process: Find low inventory stocks
low_stock_items = []
for inventory_item in inventory:
    if inventory_item["stock"] < threshold:
        low_stock_items.append(inventory_item)

# 3. Output:
if len(low_stock_items) > 0:
    print("Low stock items found:")
    for inventory_item in low_stock_items:
        print(f"- {inventory_item['name']}: {inventory_item['stock']}")
else:
    print("No low stock items.")


# ==========================================================
# CREATE
# ==========================================================

# Query 1: Place a new order for an item and quantity.

# 1. Input:
item_id = int(input("Enter the Item ID to order: "))
quantity = int(input("Enter the quantity: "))

# 2. Process: Validate and create order
selected_item = None
for inventory_item in inventory:
    if inventory_item["item_id"] == item_id:
        selected_item = inventory_item
        break

if selected_item is None:
    order_message = "Order failed: Item not found."
elif quantity <= 0:
    order_message = "Order failed: Quantity must be greater than 0."
elif selected_item["stock"] < quantity:
    order_message = f"Order failed: Not enough stock. Available: {selected_item['stock']}"
else:
    selected_item["stock"] -= quantity
    total_price = round(quantity * selected_item["unit_price"], 2)

    next_number = 101
    if len(orders) > 0:
        last_id = orders[-1]["order_id"]
        next_number = int(last_id.split("_")[1]) + 1

    new_order_id = f"Order_{next_number}"

    new_order = {
        "order_id": new_order_id,
        "item_id": item_id,
        "quantity": quantity,
        "status": "Placed",
        "total": total_price,
    }

    orders.append(new_order)
    order_message = f"Order placed successfully: {new_order_id}"

# 3. Output:
print(order_message)


# ==========================================================
# READ
# ==========================================================

# Query 2: View all orders placed for a particular item.

# 1. Input:
search_item = input("Enter the item name to search (e.g. 'Latte'): ")

# 2. Process: Find orders for item
matching_item_id = None
for inventory_item in inventory:
    if inventory_item["name"].lower() == search_item.lower():
        matching_item_id = inventory_item["item_id"]
        break

matching_orders = []
if matching_item_id is not None:
    for customer_order in orders:
        if customer_order["item_id"] == matching_item_id:
            matching_orders.append(customer_order)

# 3. Output:
if matching_item_id is None:
    print("Item not found.")
elif len(matching_orders) == 0:
    print("No orders found for that item.")
else:
    print("Matching orders:")
    for customer_order in matching_orders:
        print(customer_order)


# ==========================================================
# READ
# ==========================================================

# Query 3: Total number of orders placed for "Cold Brew".

# 1. Input:
target_name = "Cold Brew"

# 2. Process: Count orders
target_item_id = None
for inventory_item in inventory:
    if inventory_item["name"] == target_name:
        target_item_id = inventory_item["item_id"]
        break

order_count = 0
if target_item_id is not None:
    for customer_order in orders:
        if customer_order["item_id"] == target_item_id and customer_order["status"] == "Placed":
            order_count += 1

# 3. Output:
print(f"Total number of orders placed for '{target_name}': {order_count}")


# ==========================================================
# UPDATE
# ==========================================================

# Query 4: Update item stock quantity by item id.

# 1. Input:
item_id = int(input("Enter ID of item to update: "))
new_stock = int(input("Enter new stock quantity: "))

# 2. Process: Validate and update stock
item_updated = False
for inventory_item in inventory:
    if inventory_item["item_id"] == item_id:
        if new_stock >= 0:
            inventory_item["stock"] = new_stock
            item_updated = True
        break

# 3. Output:
if item_updated:
    print("Stock updated successfully.")
else:
    print("Update failed: Item not found or invalid stock.")


# ==========================================================
# REMOVE / DELETE
# ==========================================================

# Query 5: Cancel an order and restore stock.

# 1. Input:
cancel_order_id = input("Enter Order ID to cancel: ")

# 2. Process: Cancel order
order_found = None
for customer_order in orders:
    if customer_order["order_id"] == cancel_order_id:
        order_found = customer_order
        break

if order_found is None:
    cancel_message = "Cancel failed: Order not found."
elif order_found["status"] == "Cancelled":
    cancel_message = "Order already cancelled."
else:
    order_found["status"] = "Cancelled"

    for inventory_item in inventory:
        if inventory_item["item_id"] == order_found["item_id"]:
            inventory_item["stock"] += order_found["quantity"]
            break

    cancel_message = "Order cancelled and stock restored."

# 3. Output:
print(cancel_message)
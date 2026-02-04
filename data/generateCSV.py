import os
import pandas as pd
import csv, random, string
from datetime import datetime, timedelta


base_path = "D:/Downloads"
os.makedirs(base_path, exist_ok = True)

#parameters
NUM_CUSTOMERS = 2000
NUM_PRODUCTS = 300
NUM_ORDERS = 10000
NUM_ORDER_ITEMS = 25000
NUM_SESSIONS = 15000

start_date = datetime(2020, 1, 1)
end_date = datetime(2025,1,1)
date_range_days = (end_date - start_date).days

first_names = ["Alex","Sam","Taylor","Jordan","Casey","Morgan","Jamie","Riley","Jesse","Quinn",
               "Avery","Cameron","Drew","Elliot","Hayden","Kai","Logan","Rowan","Sage","Skyler"]
last_names = ["Smith","Johnson","Williams","Brown","Jones","Garcia","Miller","Davis","Rodriguez","Martinez",
              "Hernandez","Lopez","Gonzalez","Wilson","Anderson","Thomas","Taylor","Moore","Jackson","Martin"]

regions = ["US","EU","UK","CA","AU","IN"]
channels = ["Paid Social","Organic Search","Email","Referral","Direct","Influencer"]

categories = {
    "Electronics": ["Wireless Mouse","Mechanical Keyboard","Bluetooth Speaker","USB-C Cable","Laptop Stand",
                    "Webcam","Noise-Cancelling Headphones","Portable SSD","Smartwatch","Gaming Controller"],
    "Home & Kitchen": ["Ceramic Mug","Stainless Steel Pan","Electric Kettle","Kitchen Knife Set","Cutting Board",
                       "Blender","Toaster","Air Fryer","Vacuum Cleaner","Food Storage Set"],
    "Sports & Outdoors": ["Yoga Mat","Dumbbell Set","Water Bottle","Camping Tent","Hiking Backpack",
                          "Running Shoes","Fitness Tracker","Resistance Bands","Bike Helmet","Sleeping Bag"],
    "Beauty & Personal Care": ["Face Cleanser","Moisturizer","Shampoo","Conditioner","Body Lotion",
                               "Sunscreen","Lip Balm","Hair Dryer","Electric Toothbrush","Razor Set"],
    "Books": ["Productivity Book","Fantasy Novel","Sci-Fi Novel","Cookbook","Self-Help Guide",
              "Mystery Novel","Thriller Book","Biography","History Book","Programming Guide"]
}

statuses = ["pending","paid","shipped","cancelled","refunded"]
payment_methods = ["credit_card","paypal","apple_pay","google_pay","bank_transfer"]
countries = ["United States","Canada","United Kingdom","Germany","France","Australia","India","Spain","Italy","Netherlands"]
cities = ["New York","Los Angeles","Chicago","Toronto","Vancouver","London","Berlin","Paris","Sydney","Melbourne",
          "Mumbai","Bangalore","Madrid","Rome","Amsterdam"]

device_types = ["desktop","mobile","tablet"]
traffic_sources = ["Email","Paid Social","Direct","Organic Search","Ads","Push Notification"]
landing_pages = ["home","product","cart","checkout","search"]

def random_date():
    return start_date + timedelta(days=random.randint(0, date_range_days), seconds=random.randint(0,86399))

# 1. customers.csv
customers_path = os.path.join(base_path, "customer.csv")
with open(customers_path, "w", newline="", encoding="utf-8") as f:
    write = csv.writer(f)
    write.writerow(["customer_id","first_name","last_name","email","signup_date","region","acquisition_cahnnel","is_active"])
    for cid in range (1, NUM_CUSTOMERS +1): #+1 because headerrow takes a row
        fn = random.choice(first_names)
        ln = random.choice(last_names)
        email = f"{fn.lower()}.{ln.lower()}{random.randint(0,9999):04d}@realemail.com"
        signup = start_date + timedelta(days=random.randint(0, date_range_days))
        region = random.choice(regions)
        channel = random.choice(channels)
        is_active = random.random() < 0.8  # 80% chance of being active
        write.writerow([cid, fn, ln, email, signup.date().isoformat(), region, channel, str(is_active).lower()])

# 2. products.csv
products = []
products_path = os.path.join(base_path, "products.csv")
with open(products_path, "w", newline="", encoding="utf-8") as f:
    write = csv.writer(f)
    write.writerow(["product_id","product_name","category","subcategory","price","cost","is_discontinued"])
    pid = 1
    for category, names in categories.items():
        for name in names:
            if pid > NUM_PRODUCTS:
                break
            price = round(random.uniform(5, 400), 2)
            cost = round(price * random.uniform(0.4, 0.7), 2)
            discontinued = random.random() < 0.1  # 10% chance
            products.append((pid, name, category, "",  price, cost))
            write.writerow([pid, name, category, "", f"{price:.2f}", f"{cost:.2f}", str(discontinued).lower()])
            pid += 1
        if pid > NUM_PRODUCTS:
            break
#ensure we have exactly NUM_PRODUCTS by duping if needed
while len(products) < NUM_PRODUCTS:
    pid = len(products) + 1
    base = random.choice(list(categories.items()))
    category = base[0]
    name = random.choice(base[1]) + f" {pid}"
    price = round(random.uniform(5, 400), 2)
    cost = round(price * random.uniform(0.4, 0.7), 2)
    discontinued = random.random() < 0.1
    products.append((pid, name, category, "",  price, cost))
    with open(products_path, "a", newline="", encoding="utf-8") as f:
        write = csv.writer(f)
        write.writerow([pid, name, category, "", f"{price:.2f}", f"{cost:.2f}", str(discontinued).lower()])

#build lookup for product prices
product_price = {p[0]: p[4] for p in products}
product_cost = {p[0]: p[5] for p in products}

# 3. orders.csv
orders = []
orders_path = os.path.join(base_path, "orders.csv")
with open(orders_path, "w", newline="", encoding="utf-8") as f:
    write = csv.writer(f)
    write.writerow(["order_id","customer_id","order_date","status","payment_method","shipping_country","shipping_city"])
    for oid in range(1, NUM_ORDERS + 1):
        cid = random.randint(1, NUM_CUSTOMERS)
        order_dt = random_date()
        status = random.choices(statuses, weights=[0.1,0.4,0.3,0.1,0.1])[0]
        pm = random.choice(payment_methods)
        country = random.choice(countries)
        city = random.choice(cities)
        orders.append((oid, cid, order_dt, status))
        write.writerow([oid, cid, order_dt.isoformat(sep=' '), status, pm, country, city])

# 4. order_items.csv
order_items_path = os.path.join(base_path, "order_items.csv")
with open(order_items_path, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["order_item_id","order_id","product_id","quantity","unit_price","discount"])
    for iid in range(1, NUM_ORDER_ITEMS + 1):
        order = random.choice(orders)
        oid = order[0]
        pid = random.randint(1, NUM_PRODUCTS)
        qty = random.randint(1, 5)
        price = product_price[pid]
        discount = random.choice([0,0,0,5,10,15])
        writer.writerow([iid, oid, pid, qty, f"{price:.2f}", discount])

# 5. web_sessions.csv
sessions_path = os.path.join(base_path, "web_sessions.csv")
with open(sessions_path, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["session_id","customer_id","session_start","device_type","traffic_source","landed_on_page"])
    for sid in range(1, NUM_SESSIONS + 1):
        cid = random.randint(1, NUM_CUSTOMERS)
        session_dt = random_date()
        device = random.choice(device_types)
        source = random.choice(traffic_sources)
        page = random.choice(landing_pages)
        writer.writerow([sid, cid, session_dt.isoformat(sep=' '), device, source, page])

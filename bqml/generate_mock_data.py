import datetime
import json
import random
import uuid

# Configuration
NUM_USERS = 100
START_DATE = datetime.date(2023, 1, 1)
DAYS_TO_SIMULATE = 60
OUTPUT_FILE = "ga4_mock_data.json"

# Event Types
EVENTS = ["session_start", "page_view", "view_item", "add_to_cart", "begin_checkout", "purchase"]

# Items
ITEMS = [
    {"item_id": "SKU_1001", "item_name": "T-Shirt Basic", "price": 20.0, "category": "Apparel"},
    {"item_id": "SKU_1002", "item_name": "Jeans Slim", "price": 50.0, "category": "Apparel"},
    {"item_id": "SKU_2001", "item_name": "Running Shoes", "price": 80.0, "category": "Footwear"},
    {"item_id": "SKU_3001", "item_name": "Cap", "price": 15.0, "category": "Accessories"},
    {"item_id": "SKU_4001", "item_name": "Backpack", "price": 45.0, "category": "Accessories"},
]

def generate_user_data():
    """Generates a list of events for a set of users with varying behaviors."""
    
    all_events = []
    
    user_ids = [str(uuid.uuid4()) for _ in range(NUM_USERS)]
    
    # Assign personas
    # 10% Heavy Buyers
    # 30% Window Shoppers 
    # 60% Bouncers
    heavy_buyers = user_ids[:int(NUM_USERS*0.1)]
    window_shoppers = user_ids[int(NUM_USERS*0.1):int(NUM_USERS*0.1)+int(NUM_USERS*0.3)]
    bouncers = user_ids[int(NUM_USERS*0.4):]

    for day_offset in range(DAYS_TO_SIMULATE):
        current_date = START_DATE + datetime.timedelta(days=day_offset)
        date_str = current_date.strftime("%Y%m%d")
        
        # Decide which users are active today
        daily_active_users = []
        
        # Heavy buyers visit frequently (30% chance per day)
        for uid in heavy_buyers:
            if random.random() < 0.3: daily_active_users.append((uid, "buyer"))
            
        # Window shoppers visit moderately (10% chance per day)
        for uid in window_shoppers:
            if random.random() < 0.1: daily_active_users.append((uid, "shopper"))
            
        # Bouncers visit rarely (2% chance per day)
        for uid in bouncers:
            if random.random() < 0.02: daily_active_users.append((uid, "bouncer"))

        for uid, persona in daily_active_users:
            # Generate Session
            ga_session_id = int(datetime.datetime.now().timestamp()) + random.randint(1, 100000)
            
            # Base timestamp for the day (random start time)
            base_timestamp_micros = int(datetime.datetime(
                current_date.year, current_date.month, current_date.day,
                random.randint(8, 22), random.randint(0, 59)
            ).timestamp() * 1000000)

            # Common Params
            base_params = [
                {"key": "ga_session_id", "value": {"int_value": ga_session_id}},
                {"key": "page_title", "value": {"string_value": "Home Page"}}
            ]

            # 1. session_start
            all_events.append({
                "event_date": date_str,
                "event_timestamp": base_timestamp_micros,
                "event_name": "session_start",
                "user_pseudo_id": uid,
                "event_params": base_params
            })
            base_timestamp_micros += random.randint(1000, 5000000) # +1-5 seconds

            # 2. view_item (Behavior based on persona)
            num_views = 0
            if persona == "bouncer": num_views = random.randint(0, 1)
            elif persona == "shopper": num_views = random.randint(2, 5)
            elif persona == "buyer": num_views = random.randint(3, 8)

            for _ in range(num_views):
                item = random.choice(ITEMS)
                all_events.append({
                    "event_date": date_str,
                    "event_timestamp": base_timestamp_micros,
                    "event_name": "view_item",
                    "user_pseudo_id": uid,
                    "event_params": base_params + [
                         {"key": "item_id", "value": {"string_value": item["item_id"]}},
                         {"key": "price", "value": {"double_value": item["price"]}}
                    ]
                })
                base_timestamp_micros += random.randint(5000000, 30000000) # +5-30 seconds

                # Add to cart?
                atc_chance = 0.0
                if persona == "shopper": atc_chance = 0.2
                if persona == "buyer": atc_chance = 0.5
                
                if random.random() < atc_chance:
                    all_events.append({
                        "event_date": date_str,
                        "event_timestamp": base_timestamp_micros,
                        "event_name": "add_to_cart",
                        "user_pseudo_id": uid,
                        "event_params": base_params + [
                             {"key": "item_id", "value": {"string_value": item["item_id"]}},
                             {"key": "price", "value": {"double_value": item["price"]}}
                        ]
                    })
                    base_timestamp_micros += random.randint(2000000, 10000000) # +2-10 seconds

            # Purchase?
            purchase_chance = 0.0
            if persona == "buyer": purchase_chance = 0.4
            
            if random.random() < purchase_chance:
                # Assuming they bought the last item added or viewed
                pkt_value = random.choice(ITEMS)["price"] # Simple simplification
                all_events.append({
                    "event_date": date_str,
                    "event_timestamp": base_timestamp_micros,
                    "event_name": "purchase",
                    "user_pseudo_id": uid,
                    "event_params": base_params + [
                         {"key": "currency", "value": {"string_value": "USD"}},
                         {"key": "value", "value": {"double_value": pkt_value}}
                    ]
                })

    return all_events

def main():
    events = generate_user_data()
    # Sort by timestamp just in case (optional, BQ handles unsorted, but nicer for humans)
    events.sort(key=lambda x: x["event_timestamp"])
    
    with open(OUTPUT_FILE, "w") as f:
        for event in events:
            f.write(json.dumps(event) + "\n")
    
    print(f"Generated {len(events)} events in {OUTPUT_FILE}")

if __name__ == "__main__":
    main()

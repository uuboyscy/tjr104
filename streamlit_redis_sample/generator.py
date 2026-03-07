import redis
import geohash
import random
import sys
import time

def generate_data(n=100000):
    """
    Generates N random points in Taiwan, clusters them,
    calculates geohashes at various precisions, and updates Redis.
    """
    try:
        r = redis.Redis(host='localhost', port=6379, decode_responses=True)
        r.ping()
    except redis.ConnectionError:
        print("Error: Cannot connect to Redis. Ensure it is running on localhost:6379.")
        return

    # Taiwan Bounds
    min_lat, max_lat = 21.9, 25.3
    min_lon, max_lon = 120.0, 122.0
    
    print(f"Starting generation of {n} points...")
    start_time = time.time()
    
    pipe = r.pipeline()
    BATCH_SIZE = 5000
    
    for i in range(n):
        # Weighted Cloud:
        # 30% Taipei (approx 25.03, 121.5)
        # 20% Kaohsiung (approx 22.6, 120.3)
        # 20% Taichung (approx 24.1, 120.6)
        # 30% Random uniform
        
        rand = random.random()
        if rand < 0.3: # Taipei
            lat = random.gauss(25.03, 0.1)
            lon = random.gauss(121.5, 0.1)
        elif rand < 0.5: # Kaohsiung
            lat = random.gauss(22.6, 0.1)
            lon = random.gauss(120.3, 0.1)
        elif rand < 0.7: # Taichung
            lat = random.gauss(24.1, 0.1)
            lon = random.gauss(120.6, 0.1)
        else:
            lat = random.uniform(min_lat, max_lat)
            lon = random.uniform(min_lon, max_lon)
            
        # Clamp to bounds to ensure valid Geohash (optional but good practice)
        # lat = max(min_lat, min(max_lat, lat))
        # lon = max(min_lon, min(max_lon, lon))
        
        # Store at multiple precisions
        # We use a Hash for each precision level designed for fast retrieval: HGETALL population:5
        for p in [4, 5, 6, 7]:
            gh = geohash.encode(lat, lon, precision=p)
            pipe.hincrby(f"population:{p}", gh, 1)
            
        if (i + 1) % BATCH_SIZE == 0:
            pipe.execute()
            pipe = r.pipeline()
            sys.stdout.write(f"\rGenerated {i+1}/{n} points")
            sys.stdout.flush()
            
    pipe.execute()
    print(f"\nDone! Processed {n} points in {time.time() - start_time:.2f}s")
    
    # Simple verification
    count_p5 = r.hlen("population:5")
    print(f"Unique Geohashes at precision 5: {count_p5}")

if __name__ == "__main__":
    generate_data()

import os
import redis

# Redis configuration (from environment variables or defaults)
REDIS_HOST = os.getenv("REDIS_HOST", "redis")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
REDIS_QUEUE = os.getenv("REDIS_QUEUE", "ip_queue")

def fetch_ips_from_queue(count=10):
    """
    Fetch IPs from Redis queue (FIFO order).
    Pops up to 'count' IPs from the queue.
    """
    try:
        r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)
        ip_list = []
        for _ in range(count):
            ip = r.lpop(REDIS_QUEUE)
            if ip:
                ip_list.append(ip)
            else:
                break  # Stop if queue is empty
        print(f"Fetched {len(ip_list)} IP(s) from Redis queue: {ip_list}")
        return ip_list
    except redis.RedisError as e:
        print(f"Redis error while fetching IPs: {e}")
        return []

# Optional manual test
if __name__ == "__main__":
    test_ips = fetch_ips_from_queue()
    print(test_ips)

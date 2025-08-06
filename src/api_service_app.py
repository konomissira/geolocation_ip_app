from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import redis
import os

# Redis configuration
REDIS_HOST = os.getenv("REDIS_HOST", "redis")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
REDIS_QUEUE = os.getenv("REDIS_QUEUE", "ip_queue")

# Initialize Redis client
r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)

app = FastAPI(title="IP Ingestion Service", description="Accept IP addresses and queue them for processing.")

class IPItem(BaseModel):
    ip: str

class IPList(BaseModel):
    ips: list[str]

@app.get("/health")
async def health_check():
    return {"status": "ok", "message": "API is running."}

@app.post("/ingest-ip")
async def ingest_single_ip(item: IPItem):
    try:
        r.rpush(REDIS_QUEUE, item.ip)
        return {"message": f"IP {item.ip} added to queue."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to enqueue IP: {str(e)}")

@app.post("/ingest-ips")
async def ingest_multiple_ips(items: IPList):
    try:
        for ip in items.ips:
            r.rpush(REDIS_QUEUE, ip)
        return {"message": f"Added {len(items.ips)} IPs to queue."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to enqueue IPs: {str(e)}")

from fastapi import APIRouter
from fastapi.responses import StreamingResponse
import asyncio
import json
from app.services.publisher import publisher
from datetime import datetime

router = APIRouter()
def json_default(obj):
    if isinstance(obj, datetime):
        return obj.isoformat()
    raise TypeError(f"Type {type(obj)} not serializable")

async def price_stream():
    queue = asyncio.Queue()
    publisher.register(queue)
    try:
        while True:
            event = await queue.get()
            yield json.dumps(event.dict(), default=json_default) + "\n"
    finally:
        publisher.unregister(queue)

@router.get("/stream")
async def stream_prices():
    return StreamingResponse(price_stream(), media_type="application/json")
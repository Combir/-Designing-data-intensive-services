import json
import redis.asyncio as redis
from typing import Any, Callable, Optional
import asyncio

redis_client = redis.Redis(
    host="redis", port=6379, db=0,
    decode_responses=True,
    socket_timeout=2,
)


async def get_json(key: str) -> Optional[Any]:
    try:
        raw = await redis_client.get(key)
        return json.loads(raw) if raw else None
    except Exception:
        return None


async def set_json(key: str, value: Any, ttl: int = 60) -> None:
    try:
        await redis_client.setex(key, ttl, json.dumps(value, default=str))
    except Exception:
        pass


async def invalidate(key: str) -> None:
    try:
        await redis_client.delete(key)
    except Exception:
        pass


async def invalidate_pattern(pattern: str) -> None:
    """Удаляет из Redis все ключи по шаблону (например, 'product:*' или 'products:*')"""
    try:
        keys = []
        async for key in redis_client.scan_iter(match=pattern):
            keys.append(key)
        if keys:
            await redis_client.delete(*keys)
    except Exception:
        pass


async def cached(key: str, ttl: int, fetch_fn: Callable, lock_timeout: int = 10):
    # 1. Проверяем кеш
    cached_value = await get_json(key)
    if cached_value is not None:
        return cached_value
    
    lock_key = f"lock:{key}"
    acquired = False
    
    try:
        # Пытаемся захватить мьютекс для защиты от Cache Stampede
        acquired = await redis_client.set(lock_key, "1", nx=True, ex=lock_timeout)
    except Exception:
        acquired = False
    
    if not acquired:
        # Если не захватили — ждем, пока другой поток запишет данные в кеш
        for _ in range(40):  # Ждем до ~2 секунд (40 * 0.05с)
            await asyncio.sleep(0.05)
            cached_value = await get_json(key)
            if cached_value is not None:
                return cached_value
        
        # Если время ожидания вышло, а кеша всё нет — на всякий случай идем в бд сами
        value = await fetch_fn()
        return value

    # 2. Если мьютекс успешно захвачен — мы единственный поток, кто идет в БД
    try:
        value = await fetch_fn()
        await set_json(key, value, ttl)
        return value
    finally:
        # 3. Всегда освобождаем блокировку
        try:
            await redis_client.delete(lock_key)
        except Exception:
            pass
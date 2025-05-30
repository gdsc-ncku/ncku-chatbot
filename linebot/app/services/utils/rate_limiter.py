import redis
from typing import cast

from app.db.redis_client import redis_client


class RateLimiter:
    def __init__(self, max_requests: int = 100, window_seconds: int = 3600):
        self.redis: redis.Redis = redis_client
        self.max_requests = max_requests
        self.window_seconds = window_seconds

    def is_allowed(self, user_id: str) -> bool:
        key = f"rate_limit:{user_id}"
        raw = self.redis.incr(key)
        count = cast(int, raw)  # 防止 linter 哇哇叫
        if count == 1:
            self.redis.expire(key, self.window_seconds)
        return count <= self.max_requests

    def time_to_reset(self, user_id: str) -> int:
        raw = self.redis.ttl(f"rate_limit:{user_id}")
        ttl = cast(int, raw)
        return max(ttl, 0)


if __name__ == "__main__":
    # Example
    rate_limiter = RateLimiter(max_requests=5, window_seconds=60)
    user_id = "user123"

    for i in range(7):
        if rate_limiter.is_allowed(user_id):
            print(f"Request {i + 1} allowed for user {user_id}.")
        else:
            print(f"Request {i + 1} denied for user {user_id}.")
            print(f"Time to reset: {rate_limiter.time_to_reset(user_id)} seconds.")

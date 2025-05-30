from redis import Redis

redis_client: Redis = Redis(
    host="localhost",
    port=6379,
    db=0,
    decode_responses=True,
    retry_on_timeout=True,
    socket_connect_timeout=5,
    socket_timeout=5,
)

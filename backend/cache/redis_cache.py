import redis
import json
import hashlib


redis_client = redis.Redis(
    host="localhost",
    port=6379,
    db=0,
    decode_responses=True
)


def make_cache_key(kb_id, question):
    raw_key = f"{kb_id}:{question.lower().strip()}"

    return hashlib.md5(
        raw_key.encode()
    ).hexdigest()


def get_cached_answer(kb_id, question):
    key = make_cache_key(kb_id, question)

    cached = redis_client.get(key)

    if cached:
        return json.loads(cached)

    return None


def save_answer_to_cache(kb_id, question, answer):
    key = make_cache_key(kb_id, question)

    redis_client.setex(
        key,
        3600,
        json.dumps(answer)
    )
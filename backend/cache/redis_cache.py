
import json
import hashlib
import os
import redis

REDIS_AVAILABLE = False
redis_client = None

REDIS_URL = os.getenv("REDIS_URL")

if REDIS_URL:
    try:
        redis_client = redis.from_url(
            REDIS_URL,
            decode_responses=True
        )

        redis_client.ping()

        REDIS_AVAILABLE = True

        print("Redis connected")

    except Exception as e:

        print("Redis disabled:", e)

        REDIS_AVAILABLE = False
        redis_client = None

else:

    print("Redis disabled: REDIS_URL not found")


def make_cache_key(kb_id, question):

    raw_key = (
        f"{kb_id}:"
        f"{question.lower().strip()}"
    )

    return hashlib.md5(
        raw_key.encode()
    ).hexdigest()


def get_cached_answer(
    kb_id,
    question
):
    if not REDIS_AVAILABLE:
        return None

    try:

        key = make_cache_key(
            kb_id,
            question
        )

        cached = redis_client.get(key)

        if cached:
            return json.loads(cached)

    except Exception as e:

        print(
            "Redis get failed:",
            e
        )

    return None


def save_answer_to_cache(
    kb_id,
    question,
    answer
):
    if not REDIS_AVAILABLE:
        return

    try:

        key = make_cache_key(
            kb_id,
            question
        )

        redis_client.setex(
            key,
            3600,
            json.dumps(answer)
        )

    except Exception as e:

        print(
            "Redis save failed:",
            e
        )

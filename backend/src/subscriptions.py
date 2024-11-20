from .database import redis_client


def publish_new_post(post_id: int):
    redis_client.publish("new_post", f"Post {post_id} added!")

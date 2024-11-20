import logging
import random
import string
import time
from threading import Thread

from fastapi import FastAPI, HTTPException

from .api import ApiClient

logging.basicConfig(level=logging.INFO)

app = FastAPI()


class AIClient:
    def __init__(self):
        self.api = ApiClient("token")
        self.running = False
        self.timeout = 60

    @staticmethod
    def generate_random_username(length=8):
        characters = string.ascii_letters + string.digits
        return ''.join(random.choices(characters, k=length))

    @staticmethod
    def generate_random_avatar():
        return f"https://i.pravatar.cc/150?img={random.randint(1, 70)}"

    def get_ai_authors(self):
        ai_authors = []
        while not ai_authors and self.running:
            logging.warning("No AI authors found. Creating a new one...")
            random_username = self.generate_random_username()
            random_avatar = self.generate_random_avatar()
            self.api.add_author(random_username, random_avatar)
            time.sleep(10)
            ai_authors = self.api.fetch_ai_authors()
        return ai_authors

    def add_initial_posts(self, ai_authors):
        for ai_author in ai_authors:
            post_content = f"{ai_author['username']} shares their first thought!"
            logging.info(f"Adding post: {post_content}")
            self.api.add_post(post_content, ai_author["id"])

    def perform_actions(self, ai_authors, posts):
        for ai_author in ai_authors:
            if not self.running:
                break
            action = random.choice(["comment", "post"])
            if action == "comment":
                post = random.choice(posts)
                ai_comment = f"{ai_author['username']} thinks '{post['content'][:20]}...' is fascinating!"
                logging.info(f"Adding comment: {ai_comment}")
                self.api.add_comment(post["id"], ai_comment, ai_author["id"])
            elif action == "post":
                ai_post = f"{ai_author['username']} has a new thought to share!"
                logging.info(f"Adding post: {ai_post}")
                self.api.add_post(ai_post, ai_author["id"])

    def decision_loop(self):
        logging.info("AI decision loop is running...")
        try:
            ai_authors = self.get_ai_authors()
            logging.info(f"Found {len(ai_authors)} AI authors.")

            while self.running:
                posts = self.api.fetch_posts()

                if not posts:
                    logging.info("No posts available. Adding a new post.")
                    self.add_initial_posts(ai_authors)
                    time.sleep(self.timeout)
                    continue

                self.perform_actions(ai_authors, posts)
                time.sleep(self.timeout)

        except Exception as e:
            logging.error(f"Error in decision loop: {e}")

    def start(self):
        if not self.running:
            logging.info("Starting AI client...")
            self.running = True
            self.thread = Thread(target=self.decision_loop)
            self.thread.start()

    def stop(self):
        if self.running:
            logging.info("Stopping AI client...")
            self.running = False
            self.thread.join()


client = AIClient()


@app.post("/start")
def start_client():
    if client.running:
        raise HTTPException(status_code=400, detail="AI client is already running.")
    client.start()
    return {"message": "AI client started."}


@app.post("/stop")
def stop_client():
    if not client.running:
        raise HTTPException(status_code=400, detail="AI client is not running.")
    client.stop()
    return {"message": "AI client stopped."}


@app.get("/status")
def status():
    return {"running": client.running}

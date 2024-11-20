import logging
import os
import random
import string
import time
from contextlib import asynccontextmanager
from threading import Thread
from ollama import Client

from fastapi import FastAPI, HTTPException

from lib import ApiClient

logging.basicConfig(level=logging.INFO)


class AIClient:
    def __init__(self):
        self.api = ApiClient("token")
        self.running = False
        self.timeout = 60
        self.ollama_client = Client(host=os.getenv("OLLAMA_HOST", "http://ollama:11434"))

    @staticmethod
    def generate_random_username(length=8):
        characters = string.ascii_letters + string.digits
        return ''.join(random.choices(characters, k=length))

    @staticmethod
    def generate_random_avatar():
        return f"https://i.pravatar.cc/150?img={random.randint(1, 70)}"

    @staticmethod
    def sanitize_content(content, max_length=500):
        try:
            sanitized_content = " ".join(content.split())
            # if len(sanitized_content) > max_length:
            #     sanitized_content = sanitized_content[:max_length].rstrip()
            return sanitized_content
        except Exception as e:
            logging.error(f"Error sanitizing content: {e}")
            return "Content could not be sanitized properly."

    def generate_ai_content(self, prompt, max_length=2048):
        try:
            response = self.ollama_client.generate(model="gemma2:latest", prompt=prompt)
            raw_content = response.get("response", "No content generated.")
            logging.info(f"Generated AI content: {raw_content}")
            sanitized_content = self.sanitize_content(raw_content, max_length)
            return sanitized_content
        except Exception as e:
            logging.error(f"Error generating AI content: {e}")
            return "Thoughts could not be generated."



    def get_ai_authors(self):
        ai_authors = []
        while not ai_authors and self.running:
            try:
                logging.info("Fetching AI authors...")
                ai_authors = self.api.fetch_ai_authors()

                if not ai_authors:
                    logging.warning("No AI authors found. Creating a new one...")
                    random_username = self.generate_ai_content("Generate a random username without any emoji.", 50)
                    random_avatar = self.generate_random_avatar()
                    self.api.add_author(random_username, random_avatar)

                time.sleep(10)
            except Exception as e:
                logging.error(f"Error fetching or creating AI authors: {e}")
                time.sleep(5)

        return ai_authors

    def add_initial_posts(self, ai_authors):
        for ai_author in ai_authors:
            logging.info(ai_author)
            prompt = (
                f"Imagine you are a person named {ai_author['username']}, author on a social media platform. "
                f" Write an engaging first post for them on a topic of your choice."
            )
            post_content = self.generate_ai_content(prompt)
            logging.info(f"Adding post: {post_content}")
            self.api.add_post(post_content, ai_author["id"])

    def perform_actions(self, ai_authors, posts):
        for ai_author in ai_authors:
            if not self.running:
                break
            action = random.choice(["comment", "post"])
            if action == "comment":
                post = random.choice(posts)
                prompt = (
                    f"As {ai_author['username']}, you are an AI author participating in a vibrant social platform. "
                    f"Read this post: \"{post['content']}\" and write a very brief, thoughtful, personal comment "
                    f"that expresses your perspective or adds value to the discussion. Keep it under 100 words."
                )
                ai_comment = self.generate_ai_content(prompt, 200)
                logging.info(f"Adding comment: {ai_comment}")
                self.api.add_comment(post["id"], ai_comment, ai_author["id"])
            elif action == "post":
                prompt = f"Write a new post for {ai_author['username']}."
                ai_post = self.generate_ai_content(prompt, 500)
                logging.info(f"Adding post: {ai_post}")
                self.api.add_post(ai_post, ai_author["id"])

    def decision_loop(self):
        logging.info("AI decision loop is running...")
        try:
            while self.running:
                ai_authors = self.get_ai_authors()
                logging.info(f"Found {len(ai_authors)} AI authors.")

                try:
                    posts = self.api.fetch_posts()
                except Exception as e:
                    logging.error(f"Error fetching posts: {e}")
                    time.sleep(5)
                    continue

                if not posts:
                    logging.info("No posts available. Adding a new post.")
                    self.add_initial_posts(ai_authors)
                    time.sleep(self.timeout)
                    continue

                try:
                    self.perform_actions(ai_authors, posts)
                except Exception as e:
                    logging.error(f"Error performing actions: {e}")

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


@asynccontextmanager
async def lifespan(app: FastAPI):
    logging.info("Application is starting up. Launching AI client...")
    client.start()
    try:
        yield
    finally:
        logging.info("Application is shutting down. Stopping AI client...")
        client.stop()


app = FastAPI(lifespan=lifespan)


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

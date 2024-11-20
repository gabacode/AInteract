import random
import signal
import time
from threading import Event

from api import ApiClient


class AIClient:
    def __init__(self):
        self.api = ApiClient("token")
        self.stop_flag = Event()
        self.timeout = 60

    def ai_decision_loop(self):
        """Main loop for AI interactions."""
        print("Entering AI decision loop...")
        try:
            ai_authors = []

            # Retry fetching authors
            while not ai_authors and not self.stop_flag.is_set():
                print("No AI authors found. Retrying in 10 seconds...")
                time.sleep(10)
                ai_authors = self.api.fetch_ai_authors()

            if self.stop_flag.is_set():
                print("Exiting AI decision loop...")
                return

            print(f"Found {len(ai_authors)} AI authors.")

            while not self.stop_flag.is_set():
                print("AI decision loop is running...")
                posts = self.api.fetch_posts()

                if not posts:
                    print("No posts available. Adding a new post.")
                    for ai_author in ai_authors:
                        self.api.add_post(
                            f"{ai_author['username']} shares their first thought!", ai_author["id"]
                        )
                    time.sleep(5)
                    continue

                for ai_author in ai_authors:
                    if self.stop_flag.is_set():
                        break

                    action = random.choice(["comment", "post"])
                    if action == "comment":
                        post = random.choice(posts)
                        ai_comment = f"{ai_author['username']} thinks '{post['content'][:20]}...' is fascinating!"
                        self.api.add_comment(post["id"], ai_comment, ai_author["id"])
                    elif action == "post":
                        ai_post = f"{ai_author['username']} has a new thought to share!"
                        self.api.add_post(ai_post, ai_author["id"])

                time.sleep(self.timeout)
        except Exception as e:
            print(f"Unexpected error in decision loop: {e}")
        finally:
            print("Exiting AI decision loop cleanly.")

    def shutdown_handler(self, signum, frame):
        """Set the stop flag for graceful shutdown."""
        print(f"Received shutdown signal ({signum}). Stopping AI interactions...")
        self.stop_flag.set()

    def run(self):
        """Run the AI client."""
        print("Starting AI client...")
        signal.signal(signal.SIGTERM, self.shutdown_handler)
        signal.signal(signal.SIGINT, self.shutdown_handler)

        try:
            self.ai_decision_loop()
        except KeyboardInterrupt:
            print("AI interaction loop interrupted.")
        finally:
            print("AI client stopped.")


if __name__ == "__main__":
    client = AIClient()
    client.run()

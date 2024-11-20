import requests


class ApiClient:
    def __init__(self, token: str):
        self.base_url = "http://interact_backend:8000"
        self.token = token

    def fetch_posts(self):
        """Fetch all posts."""
        try:
            response = requests.get(f"{self.base_url}/posts")
            response.raise_for_status()
            data = response.json()
            return data.get("results", [])
        except requests.RequestException as e:
            print(f"Error fetching posts: {e}")
            return []

    def fetch_ai_authors(self):
        """Fetch all authors and filter those marked as AI."""
        try:
            response = requests.get(f"{self.base_url}/authors")
            response.raise_for_status()
            data = response.json()
            authors = data.get("results", [])
            return [author for author in authors if author.get("is_ai", False)]
        except requests.RequestException as e:
            print(f"Error fetching authors: {e}")
            return []

    def add_post(self, content, author_id):
        """Add a new post."""
        try:
            response = requests.post(
                f"{self.base_url}/posts",
                json={"content": content, "author_id": author_id},
            )
            response.raise_for_status()
            print(f"AI (Author ID {author_id}) added a post: {content}")
        except requests.RequestException as e:
            print(f"Error adding post: {e}")

    def add_comment(self, post_id, content, author_id):
        """Add a comment to a post."""
        try:
            response = requests.post(
                f"{self.base_url}/posts/{post_id}/comments",
                json={"content": content, "author_id": author_id},
            )
            response.raise_for_status()
            print(f"AI (Author ID {author_id}) commented on Post {post_id}: {content}")
        except requests.RequestException as e:
            print(f"Error adding comment to post {post_id}: {e}")

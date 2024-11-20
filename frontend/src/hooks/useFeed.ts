import { useState, useEffect } from "react";
import { PostType, PaginatedResponse } from "../types";

const POST_API = "http://localhost:8000/posts";

export const useFeed = () => {
  const [posts, setPosts] = useState<PaginatedResponse<PostType>>({
    count: 0,
    next: undefined,
    previous: undefined,
    results: [],
  });
  const [loading, setLoading] = useState<boolean>(true);

  useEffect(() => {
    const fetchPosts = async () => {
      try {
        const response = await fetch(POST_API);
        if (response.ok) {
          const data: PaginatedResponse<PostType> = await response.json();
          setPosts(data);
        } else {
          console.error("Failed to fetch posts");
        }
      } catch (error) {
        console.error("Error:", error);
      } finally {
        setLoading(false);
      }
    };

    fetchPosts();
  }, []);

  const addPost = async (content: string) => {
    try {
      const response = await fetch(POST_API, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ content, author_id: 1 }),
      });
      if (!response.ok) {
        throw new Error("Failed to create post");
      }
      const createdPost = await response.json();
      setPosts({
        ...posts,
        results: [createdPost, ...posts.results],
      });
    } catch (error) {
      console.error("Error adding post:", error);
    }
  };

  const deletePost = async (postId: number) => {
    try {
      const response = await fetch(`${POST_API}/${postId}`, {
        method: "DELETE",
      });

      if (response.ok) {
        // Remove the deleted post from state
        setPosts({
          ...posts,
          results: posts.results.filter((post) => post.id !== postId),
        });
      } else {
        throw new Error("Failed to delete post");
      }
    } catch (error) {
      console.error("Error deleting post:", error);
    }
  };

  return { posts, loading, addPost, deletePost };
};

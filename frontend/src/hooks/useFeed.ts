import { useState, useEffect, useCallback } from "react";
import { PostType, PaginatedResponse, CommentType } from "../types";

const POST_API = "http://localhost:8000/posts";
const COMMENT_API = (postId: number) => `${POST_API}/${postId}/comments`;

export const useFeed = () => {
  const [posts, setPosts] = useState<PaginatedResponse<PostType>>({
    count: 0,
    next: undefined,
    previous: undefined,
    results: [],
  });
  const [loading, setLoading] = useState<boolean>(true);
  const [comments, setComments] = useState<Record<number, CommentType[]>>({});

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

  const fetchComments = useCallback(
    async (postId: number) => {
      try {
        const response = await fetch(`${POST_API}/${postId}/comments`);
        if (response.ok) {
          const data: CommentType[] = await response.json();
          setComments((prev) => ({ ...prev, [postId]: data }));
          return data;
        } else {
          throw new Error("Failed to fetch comments");
        }
      } catch (error) {
        console.error("Error fetching comments:", error);
        return [];
      }
    },
    [] // Ensures fetchComments is memoized
  );

  const addComment = async (
    postId: number,
    content: string,
    authorId: number
  ): Promise<CommentType> => {
    const response = await fetch(COMMENT_API(postId), {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ content, author_id: authorId }),
    });

    if (!response.ok) {
      throw new Error("Failed to add comment");
    }

    const newComment: CommentType = await response.json();

    setComments((prev) => ({
      ...prev,
      [postId]: [...(prev[postId] || []), newComment],
    }));

    return newComment;
  };

  const deleteComment = async (postId: number, commentId: number) => {
    try {
      const response = await fetch(
        `${POST_API}/${postId}/comments/${commentId}`,
        {
          method: "DELETE",
        }
      );

      if (response.ok) {
        setComments((prev) => ({
          ...prev,
          [postId]:
            prev[postId]?.filter((comment) => comment.id !== commentId) || [],
        }));
        return true;
      } else {
        throw new Error("Failed to delete comment");
      }
    } catch (error) {
      console.error(`Error deleting comment ${commentId}:`, error);
      return false;
    }
  };
  const actions = [
    {
      label: "Report",
      onClick: (postId: number) => {
        alert(`Post ${postId} reported.`);
      },
    },
    {
      label: "Delete",
      onClick: (postId: number) => {
        deletePost(postId);
      },
      className: "text-danger",
    },
  ];

  const commentActions = [
    {
      label: "Report",
      onClick: (postId: number, commentId: number) => {
        alert(`Comment ${commentId} on Post ${postId} reported.`);
      },
    },
    {
      label: "Delete",
      onClick: (postId: number, commentId: number) => {
        deleteComment(postId, commentId);
      },
      className: "text-danger",
    },
  ];

  return {
    posts,
    loading,
    addPost,
    fetchComments,
    addComment,
    comments,
    actions,
    commentActions,
  };
};

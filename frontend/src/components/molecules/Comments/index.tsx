import { useEffect, useState, FormEvent } from "react";
import { CommentType } from "../../../types";
import { Avatar } from "../../atoms/Avatar";
import { AuthorDetails } from "../../atoms/AuthorDetails";
import { PostContent } from "../../atoms/PostContent";

import "./index.scss";

interface CommentsProps {
  postId: number;
  fetchComments: (postId: number) => Promise<CommentType[]>;
  addComment: (
    postId: number,
    content: string,
    authorId: number
  ) => Promise<CommentType>;
}

export const Comments = ({
  postId,
  fetchComments,
  addComment,
}: CommentsProps) => {
  const [comments, setComments] = useState<CommentType[]>([]);
  const [newComment, setNewComment] = useState<string>("");

  useEffect(() => {
    fetchComments(postId).then(setComments);
  }, [postId]);

  const handleSubmit = async (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    if (newComment.trim() === "") return;

    const authorId = 1;
    try {
      const createdComment = await addComment(postId, newComment, authorId);
      setComments((prev) => [...prev, createdComment]);
      setNewComment("");
    } catch (error) {
      console.error("Error adding comment:", error);
    }
  };

  const Comment = ({ comment }: { comment: CommentType }) => (
    <div key={`${postId}_${comment.id}`} className="comment-card">
      <Avatar src={comment.author.avatar} alt={comment.author.username} />
      <div>
        <AuthorDetails
          username={comment.author.username}
          isAi={comment.author.is_ai}
          timestamp={comment.timestamp}
        />
        <PostContent content={comment.content} />
      </div>
    </div>
  );

  return (
    <div className="comments-section">
      <div className="comments-list">
        {comments?.map((comment) => (
          <Comment comment={comment} />
        ))}
      </div>
      <form className="add-comment-container" onSubmit={handleSubmit}>
        <input
          type="text"
          placeholder="Add a comment..."
          value={newComment}
          onChange={(e) => setNewComment(e.target.value)}
          className="add-comment-input"
        />
        <button type="submit" className="add-comment-btn">
          Comment
        </button>
      </form>
    </div>
  );
};
